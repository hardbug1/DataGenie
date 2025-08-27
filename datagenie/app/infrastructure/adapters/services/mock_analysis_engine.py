"""
Mock Analysis Engine

개발 및 테스트용 임시 분석 엔진
실제 LLM 통합 전까지 사용
"""

import asyncio
from typing import Dict, Any, Optional
import structlog

from app.domain.interfaces.services.analysis_engine import IAnalysisEngine
from app.domain.value_objects.analysis_result import AnalysisResult

logger = structlog.get_logger(__name__)


class MockAnalysisEngine(IAnalysisEngine):
    """
    Mock 분석 엔진
    
    Clean Architecture: 도메인 인터페이스의 임시 구현체
    실제 LLM 및 데이터 분석 로직 구현 전까지 더미 데이터 반환
    """
    
    def __init__(self):
        """Mock 분석 엔진 초기화"""
        logger.info("Mock Analysis Engine 초기화")
    
    async def execute_analysis(
        self,
        question: str,
        connection_id: Optional[str] = None,
        file_data: Optional[bytes] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        분석 실행 (Mock 구현)
        
        Args:
            question: 사용자 질문
            connection_id: 데이터베이스 연결 ID
            file_data: 파일 데이터
            options: 추가 옵션
            
        Returns:
            Mock 분석 결과
        """
        logger.info(
            "Mock 분석 실행 시작",
            question=question[:50] + "..." if len(question) > 50 else question,
            has_connection=connection_id is not None,
            has_file=file_data is not None
        )
        
        # 실제 분석 시간을 시뮬레이션
        await asyncio.sleep(0.5)
        
        # 질문 유형에 따른 Mock 결과 생성
        if file_data:
            return self._create_excel_analysis_result(question)
        elif connection_id:
            return self._create_database_analysis_result(question)
        else:
            return self._create_general_analysis_result(question)
    
    async def analyze_question(self, question: str) -> Dict[str, Any]:
        """
        질문 분석 (Mock 구현)
        
        Args:
            question: 사용자 질문
            
        Returns:
            Mock 질문 분석 결과
        """
        logger.debug("Mock 질문 분석", question=question)
        
        # 간단한 키워드 기반 분석
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ['매출', '판매', 'sales']):
            return {
                "type": "DB_QUERY",
                "intent": "매출 데이터 조회 및 분석",
                "entities": {
                    "metric": "매출",
                    "time_period": "최근",
                    "visualization": "차트"
                },
                "confidence": 0.85,
                "suggested_tables": ["orders", "sales"]
            }
        elif any(keyword in question_lower for keyword in ['파일', '엑셀', 'excel']):
            return {
                "type": "EXCEL_ANALYSIS",
                "intent": "파일 데이터 분석",
                "entities": {
                    "data_source": "파일",
                    "analysis_type": "통계"
                },
                "confidence": 0.90,
                "suggested_tables": []
            }
        else:
            return {
                "type": "GENERAL",
                "intent": "일반적인 질문",
                "entities": {},
                "confidence": 0.70,
                "suggested_tables": []
            }
    
    def _create_database_analysis_result(self, question: str) -> AnalysisResult:
        """데이터베이스 분석 결과 생성"""
        return AnalysisResult(
            analysis_type="database",
            question=question,
            sql_query="SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as total_sales FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '3 months' GROUP BY month ORDER BY month",
            execution_success=True,
            data=[
                {"month": "2024-01-01T00:00:00Z", "total_sales": 125000.50},
                {"month": "2024-02-01T00:00:00Z", "total_sales": 142300.75},
                {"month": "2024-03-01T00:00:00Z", "total_sales": 158750.25}
            ],
            columns=["month", "total_sales"],
            row_count=3,
            chart_type="line",
            chart_config={
                "x_axis": "month",
                "y_axis": "total_sales",
                "title": "월별 매출 추이",
                "color_scheme": "blue"
            },
            summary="최근 3개월간 매출이 지속적으로 증가하고 있습니다.",
            insights=[
                "2월 매출이 1월 대비 13.8% 증가했습니다",
                "3월 매출이 2월 대비 11.6% 증가했습니다",
                "전체적으로 상승 추세를 보이고 있습니다"
            ],
            recommendations=[
                "현재 증가 추세를 유지하기 위한 마케팅 전략을 강화하세요",
                "4월 매출 목표를 175,000으로 설정하는 것을 권장합니다"
            ],
            metadata={
                "execution_time_ms": 500,
                "cache_used": False,
                "data_source": "mock_database"
            }
        )
    
    def _create_excel_analysis_result(self, question: str) -> AnalysisResult:
        """Excel 분석 결과 생성"""
        return AnalysisResult(
            analysis_type="excel",
            question=question,
            generated_code="df.groupby('category')['sales'].sum().sort_values(ascending=False)",
            execution_success=True,
            data=[
                {"category": "전자제품", "sales": 250000},
                {"category": "의류", "sales": 180000},
                {"category": "도서", "sales": 95000}
            ],
            columns=["category", "sales"],
            row_count=3,
            chart_type="bar",
            chart_config={
                "x_axis": "category",
                "y_axis": "sales",
                "title": "카테고리별 매출",
                "color_scheme": "green"
            },
            summary="전자제품 카테고리가 가장 높은 매출을 기록했습니다.",
            insights=[
                "전자제품이 전체 매출의 47.6%를 차지합니다",
                "의류가 두 번째로 높은 매출을 기록했습니다",
                "상위 2개 카테고리가 전체 매출의 82%를 차지합니다"
            ],
            recommendations=[
                "전자제품 카테고리의 재고를 늘리는 것을 고려하세요",
                "도서 카테고리의 마케팅을 강화할 필요가 있습니다"
            ],
            metadata={
                "execution_time_ms": 300,
                "file_processed": True,
                "data_source": "uploaded_file"
            }
        )
    
    def _create_general_analysis_result(self, question: str) -> AnalysisResult:
        """일반 질문 분석 결과 생성"""
        return AnalysisResult(
            analysis_type="general",
            question=question,
            execution_success=True,
            summary="DataGenie는 자연어로 데이터를 분석할 수 있는 AI 분석 도구입니다.",
            insights=[
                "데이터베이스 연결을 통해 SQL 쿼리를 자동 생성합니다",
                "Excel 파일을 업로드하여 즉시 분석할 수 있습니다",
                "결과를 다양한 차트로 시각화합니다"
            ],
            recommendations=[
                "구체적인 데이터 질문을 해보세요",
                "데이터베이스를 연결하거나 Excel 파일을 업로드해보세요"
            ],
            metadata={
                "execution_time_ms": 100,
                "response_type": "help",
                "data_source": "system"
            }
        )
