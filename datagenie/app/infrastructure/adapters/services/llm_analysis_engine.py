"""
LLM-based Analysis Engine Implementation

Clean Architecture: Infrastructure Layer
LLM을 활용한 실제 분석 엔진 구현
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from app.domain.interfaces.services.analysis_engine import IAnalysisEngine
from app.domain.value_objects.analysis_result import AnalysisResult
from app.core.nlp.llm_processor import (
    DataGenieLLMProcessor,
    SQLGenerationResult,
    ExcelAnalysisResult,
    LLMProcessingError
)
from app.core.security.pii_masker import PIIMasker

logger = structlog.get_logger(__name__)


class LLMAnalysisEngine(IAnalysisEngine):
    """
    LLM 기반 분석 엔진
    
    Clean Architecture: Infrastructure Layer
    도메인 인터페이스를 구현하여 실제 LLM 분석 기능 제공
    """
    
    def __init__(self, cache_client=None):
        """
        LLM 분석 엔진 초기화
        
        Args:
            cache_client: Redis 캐시 클라이언트 (선택사항)
        """
        self.llm_processor = DataGenieLLMProcessor(cache_client)
        self.pii_masker = PIIMasker()
        
        # 예시 쿼리 데이터베이스 (실제로는 외부 저장소에서 로드)
        self.example_queries = [
            {
                "question": "지난 3개월 매출 추이를 보여주세요",
                "sql": "SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY month ORDER BY month"
            },
            {
                "question": "가장 많이 팔린 상품 10개를 알려주세요",
                "sql": "SELECT p.name, COUNT(oi.product_id) as sales_count FROM products p JOIN order_items oi ON p.id = oi.product_id GROUP BY p.id, p.name ORDER BY sales_count DESC LIMIT 10"
            },
            {
                "question": "월별 신규 고객 수를 분석해주세요",
                "sql": "SELECT DATE_TRUNC('month', created_at) as month, COUNT(*) as new_customers FROM users GROUP BY month ORDER BY month"
            }
        ]
    
    async def execute_analysis(
        self,
        question: str,
        user_id: str,
        connection_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        분석 실행
        
        Args:
            question: 자연어 질문
            user_id: 사용자 ID
            connection_id: 데이터베이스 연결 ID (선택사항)
            options: 분석 옵션
            
        Returns:
            AnalysisResult: 분석 결과
        """
        start_time = datetime.now()
        options = options or {}
        
        try:
            logger.info(
                "분석 실행 시작",
                extra={
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "question_length": len(question)
                }
            )
            
            # 1. 질문 분류
            classification = await self.llm_processor.classify_question(question)
            
            logger.info(
                "질문 분류 완료",
                extra={
                    "analysis_type": classification.analysis_type,
                    "confidence": classification.confidence,
                    "complexity": classification.complexity
                }
            )
            
            # 2. 분석 유형에 따른 처리
            if classification.analysis_type == "database":
                result = await self._execute_database_analysis(
                    question, user_id, connection_id, options, classification
                )
            elif classification.analysis_type == "excel":
                result = await self._execute_excel_analysis(
                    question, user_id, options, classification
                )
            else:
                result = await self._execute_general_analysis(
                    question, user_id, options, classification
                )
            
            # 3. 개인정보 마스킹 적용
            masked_result = self._apply_pii_masking(result, user_id)
            
            # 4. 처리 시간 계산
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            logger.info(
                "분석 실행 완료",
                extra={
                    "user_id": user_id,
                    "analysis_type": classification.analysis_type,
                    "processing_time_ms": processing_time,
                    "success": masked_result.execution_success
                }
            )
            
            return masked_result
            
        except Exception as e:
            logger.error(
                "분석 실행 실패",
                extra={
                    "user_id": user_id,
                    "error": str(e),
                    "question_hash": hash(question) % 10000
                }
            )
            
            # 실패 시 기본 응답 반환
            return AnalysisResult(
                analysis_type="error",
                question=question,
                execution_success=False,
                summary=f"분석 실행 중 오류가 발생했습니다: {str(e)}",
                metadata={
                    "error_type": type(e).__name__,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
    
    async def _execute_database_analysis(
        self,
        question: str,
        user_id: str,
        connection_id: Optional[str],
        options: Dict[str, Any],
        classification
    ) -> AnalysisResult:
        """데이터베이스 분석 실행"""
        
        # 스키마 정보 가져오기 (실제로는 connection_id로 조회)
        schema_info = self._get_mock_schema_info(connection_id)
        
        try:
            # SQL 생성
            sql_result = await self.llm_processor.generate_sql_analysis(
                question=question,
                schema_info=schema_info,
                examples=self.example_queries,
                user_context={"user_id": user_id, "connection_id": connection_id}
            )
            
            # 실제로는 데이터베이스에서 쿼리 실행
            # 현재는 모의 데이터 생성
            mock_data = self._generate_mock_database_result(sql_result)
            
            return AnalysisResult(
                analysis_type="database",
                question=question,
                sql_query=sql_result.sql,
                execution_success=True,
                data=mock_data["data"],
                columns=mock_data["columns"],
                row_count=len(mock_data["data"]),
                summary=sql_result.explanation,
                insights=self._generate_insights(mock_data["data"], sql_result),
                recommendations=self._generate_recommendations(sql_result),
                metadata={
                    "confidence": sql_result.confidence,
                    "complexity": sql_result.complexity,
                    "tables_used": sql_result.tables_used,
                    "processing_time_ms": sql_result.processing_time_ms,
                    "warnings": sql_result.warnings
                }
            )
            
        except LLMProcessingError as e:
            return AnalysisResult(
                analysis_type="database",
                question=question,
                execution_success=False,
                summary=f"SQL 생성 실패: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _execute_excel_analysis(
        self,
        question: str,
        user_id: str,
        options: Dict[str, Any],
        classification
    ) -> AnalysisResult:
        """Excel 분석 실행"""
        
        # 데이터프레임 정보 가져오기 (실제로는 업로드된 파일에서)
        df_info = self._get_mock_dataframe_info(options.get("file_path"))
        
        try:
            # Python 코드 생성
            excel_result = await self.llm_processor.generate_excel_analysis(
                question=question,
                dataframe_info=df_info,
                sample_data=self._get_sample_data(df_info),
                user_context={"user_id": user_id}
            )
            
            # 실제로는 생성된 코드를 안전한 환경에서 실행
            # 현재는 모의 결과 생성
            mock_result = self._execute_mock_python_code(excel_result)
            
            return AnalysisResult(
                analysis_type="excel",
                question=question,
                generated_code=excel_result.code,
                execution_success=True,
                data=mock_result["data"],
                columns=mock_result["columns"],
                row_count=len(mock_result["data"]),
                chart_type=excel_result.visualization_type,
                chart_config=self._generate_chart_config(excel_result),
                summary=excel_result.explanation,
                insights=self._generate_excel_insights(mock_result, excel_result),
                metadata={
                    "confidence": excel_result.confidence,
                    "complexity": excel_result.complexity,
                    "safety_check": excel_result.safety_check,
                    "processing_time_ms": excel_result.processing_time_ms
                }
            )
            
        except LLMProcessingError as e:
            return AnalysisResult(
                analysis_type="excel",
                question=question,
                execution_success=False,
                summary=f"Excel 분석 코드 생성 실패: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _execute_general_analysis(
        self,
        question: str,
        user_id: str,
        options: Dict[str, Any],
        classification
    ) -> AnalysisResult:
        """일반 분석 실행"""
        
        return AnalysisResult(
            analysis_type="general",
            question=question,
            execution_success=True,
            summary=f"'{question}'에 대한 일반적인 분석입니다. 더 구체적인 분석을 위해서는 데이터베이스 연결이나 Excel 파일이 필요합니다.",
            recommendations=[
                "데이터베이스에 연결하여 SQL 기반 분석을 수행해보세요",
                "Excel 파일을 업로드하여 데이터 분석을 수행해보세요",
                "더 구체적인 질문으로 다시 시도해보세요"
            ],
            metadata={
                "classification": classification.__dict__,
                "user_id": user_id
            }
        )
    
    def _apply_pii_masking(self, result: AnalysisResult, user_id: str) -> AnalysisResult:
        """개인정보 마스킹 적용"""
        try:
            # 데이터에 PII 마스킹 적용
            if result.data:
                masking_result = self.pii_masker.mask_data(
                    result.data,
                    context={"user_id": user_id, "analysis_type": result.analysis_type}
                )
                
                if masking_result.masking_applied:
                    logger.info(
                        "개인정보 마스킹 적용",
                        extra={
                            "user_id": user_id,
                            "pii_detected": len(masking_result.detected_pii),
                            "analysis_type": result.analysis_type
                        }
                    )
                    
                    # 마스킹된 데이터로 결과 업데이트
                    return AnalysisResult(
                        analysis_type=result.analysis_type,
                        question=result.question,
                        sql_query=result.sql_query,
                        generated_code=result.generated_code,
                        execution_success=result.execution_success,
                        data=masking_result.masked_data,
                        columns=result.columns,
                        row_count=result.row_count,
                        chart_type=result.chart_type,
                        chart_config=result.chart_config,
                        chart_data=result.chart_data,
                        summary=result.summary,
                        insights=result.insights,
                        recommendations=result.recommendations,
                        metadata={
                            **(result.metadata or {}),
                            "pii_masking_applied": True,
                            "pii_types_detected": [pii.pii_type.value for pii in masking_result.detected_pii]
                        }
                    )
            
            return result
            
        except Exception as e:
            logger.warning(f"PII 마스킹 실패: {str(e)}")
            return result
    
    def _get_mock_schema_info(self, connection_id: Optional[str]) -> Dict[str, Any]:
        """모의 스키마 정보 생성"""
        return {
            "users": {
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "username", "type": "varchar", "nullable": False},
                    {"name": "email", "type": "varchar", "nullable": False},
                    {"name": "created_at", "type": "timestamp", "nullable": False}
                ]
            },
            "orders": {
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "user_id", "type": "integer", "foreign_key": "users.id"},
                    {"name": "amount", "type": "decimal", "nullable": False},
                    {"name": "status", "type": "varchar", "nullable": False},
                    {"name": "order_date", "type": "timestamp", "nullable": False}
                ]
            },
            "products": {
                "columns": [
                    {"name": "id", "type": "integer", "primary_key": True},
                    {"name": "name", "type": "varchar", "nullable": False},
                    {"name": "price", "type": "decimal", "nullable": False},
                    {"name": "category", "type": "varchar", "nullable": True}
                ]
            }
        }
    
    def _get_mock_dataframe_info(self, file_path: Optional[str]) -> Dict[str, Any]:
        """모의 데이터프레임 정보 생성"""
        return {
            "row_count": 1000,
            "column_count": 5,
            "columns": {
                "날짜": {"dtype": "datetime64", "null_count": 0},
                "매출": {"dtype": "float64", "null_count": 5},
                "제품명": {"dtype": "object", "null_count": 0},
                "카테고리": {"dtype": "object", "null_count": 10},
                "수량": {"dtype": "int64", "null_count": 2}
            }
        }
    
    def _get_sample_data(self, df_info: Dict[str, Any]) -> str:
        """샘플 데이터 생성"""
        return """
날짜,매출,제품명,카테고리,수량
2024-01-01,150000,노트북,전자제품,5
2024-01-02,80000,마우스,전자제품,20
2024-01-03,200000,키보드,전자제품,15
        """
    
    def _generate_mock_database_result(self, sql_result: SQLGenerationResult) -> Dict[str, Any]:
        """모의 데이터베이스 결과 생성"""
        return {
            "data": [
                {"month": "2024-01", "total_sales": 1500000},
                {"month": "2024-02", "total_sales": 1800000},
                {"month": "2024-03", "total_sales": 2100000}
            ],
            "columns": ["month", "total_sales"]
        }
    
    def _execute_mock_python_code(self, excel_result: ExcelAnalysisResult) -> Dict[str, Any]:
        """모의 Python 코드 실행 결과"""
        return {
            "data": [
                {"제품명": "노트북", "총매출": 3000000},
                {"제품명": "마우스", "총매출": 800000},
                {"제품명": "키보드", "총매출": 1200000}
            ],
            "columns": ["제품명", "총매출"]
        }
    
    def _generate_insights(self, data: List[Dict], sql_result: SQLGenerationResult) -> List[str]:
        """인사이트 생성"""
        insights = []
        
        if data and len(data) > 1:
            insights.append(f"총 {len(data)}개의 결과가 조회되었습니다")
            
            if sql_result.complexity == "complex":
                insights.append("복잡한 쿼리로 인해 처리 시간이 다소 소요되었습니다")
            
            if sql_result.requires_join:
                insights.append("여러 테이블을 조인하여 종합적인 분석을 수행했습니다")
        
        return insights
    
    def _generate_recommendations(self, sql_result: SQLGenerationResult) -> List[str]:
        """추천사항 생성"""
        recommendations = []
        
        if sql_result.confidence < 0.8:
            recommendations.append("결과의 신뢰도가 낮습니다. 질문을 더 구체적으로 해보세요")
        
        if sql_result.warnings:
            recommendations.extend([f"주의사항: {warning}" for warning in sql_result.warnings])
        
        if sql_result.complexity == "complex":
            recommendations.append("복잡한 분석입니다. 결과를 단계별로 검토해보세요")
        
        return recommendations
    
    def _generate_excel_insights(self, result: Dict[str, Any], excel_result: ExcelAnalysisResult) -> List[str]:
        """Excel 분석 인사이트 생성"""
        insights = []
        
        if result["data"]:
            insights.append(f"Excel 데이터에서 {len(result['data'])}개의 결과를 분석했습니다")
        
        if excel_result.visualization_type != "none":
            insights.append(f"{excel_result.visualization_type} 차트로 시각화가 가능합니다")
        
        return insights
    
    def _generate_chart_config(self, excel_result: ExcelAnalysisResult) -> Optional[Dict[str, Any]]:
        """차트 설정 생성"""
        if excel_result.visualization_type == "none":
            return None
        
        return {
            "type": excel_result.visualization_type,
            "title": "분석 결과 차트",
            "x_axis": "카테고리",
            "y_axis": "값"
        }
