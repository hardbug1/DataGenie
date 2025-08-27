"""
DataGenie LLM Processor

Clean Architecture: Application Core
LLM 통합 및 자연어 처리 핵심 로직
"""

import json
import hashlib
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import structlog

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import tiktoken

from app.core.nlp.prompt_templates import DataGeniePromptTemplates, PromptInjectionDetector
from app.core.security.sql_validator import SQLSecurityValidator, SQLValidationResult
from app.config.settings import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()


@dataclass(frozen=True)
class SQLGenerationResult:
    """SQL 생성 결과"""
    sql: str
    explanation: str
    estimated_rows: int
    confidence: float
    warnings: List[str]
    tables_used: List[str]
    requires_join: bool
    complexity: str
    processing_time_ms: int
    
    def is_high_confidence(self) -> bool:
        """높은 신뢰도인지 확인"""
        return self.confidence >= 0.8
    
    def is_complex_query(self) -> bool:
        """복잡한 쿼리인지 확인"""
        return self.complexity == "complex" or self.requires_join


@dataclass(frozen=True)
class ExcelAnalysisResult:
    """Excel 분석 결과"""
    code: str
    explanation: str
    expected_output: str
    confidence: float
    safety_check: str
    visualization_type: str
    complexity: str
    processing_time_ms: int
    
    def is_safe_to_execute(self) -> bool:
        """실행 안전성 확인"""
        return self.safety_check == "confirmed_safe" and self.confidence >= 0.7


@dataclass(frozen=True)
class QuestionClassificationResult:
    """질문 분류 결과"""
    analysis_type: str
    confidence: float
    reasoning: str
    keywords: List[str]
    requires_data_connection: bool
    complexity: str
    estimated_processing_time: str


class DataGenieLLMProcessor:
    """
    DataGenie 전용 LLM 프로세서
    
    LLM Integration 규칙 준수:
    - 안전한 LLM 호출 패턴
    - 프롬프트 인젝션 방지
    - 출력 검증 및 신뢰도 평가
    """
    
    def __init__(self, cache_client=None):
        """
        LLM 프로세서 초기화
        
        Args:
            cache_client: Redis 캐시 클라이언트 (선택사항)
        """
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.0,  # 결정적 출력
            max_tokens=settings.openai_max_tokens,
            timeout=30,  # 30초 타임아웃
            max_retries=2,  # 재시도 횟수
            openai_api_key=settings.openai_api_key
        )
        
        self.fallback_llm = ChatOpenAI(
            model=settings.openai_model_fallback,
            temperature=0.0,
            max_tokens=settings.openai_max_tokens,
            timeout=30,
            max_retries=1,
            openai_api_key=settings.openai_api_key
        )
        
        self.prompt_templates = DataGeniePromptTemplates()
        self.injection_detector = PromptInjectionDetector()
        self.sql_validator = SQLSecurityValidator()
        self.cache_client = cache_client
        self.token_encoder = tiktoken.encoding_for_model(settings.openai_model)
        
        # 성능 메트릭
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'cache_hits': 0,
            'total_tokens_used': 0,
            'average_confidence': 0.0
        }
    
    async def generate_sql_analysis(
        self,
        question: str,
        schema_info: Dict[str, Any],
        examples: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> SQLGenerationResult:
        """
        자연어 질문을 SQL 쿼리로 변환
        
        Args:
            question: 사용자 질문
            schema_info: 데이터베이스 스키마 정보
            examples: 예시 쿼리 목록
            user_context: 사용자 컨텍스트 정보
            
        Returns:
            SQLGenerationResult: SQL 생성 결과
        """
        start_time = datetime.now()
        
        try:
            # 1. 입력 검증
            self._validate_input(question)
            
            # 2. 프롬프트 인젝션 검사
            if self.injection_detector.detect_injection(question):
                raise SecurityError("프롬프트 인젝션 시도가 감지되었습니다")
            
            # 3. 캐시 확인
            cache_key = self._generate_cache_key("sql", question, schema_info)
            cached_result = await self._get_cached_result(cache_key)
            if cached_result:
                self.metrics['cache_hits'] += 1
                return cached_result
            
            # 4. 프롬프트 구성
            formatted_schema = self.prompt_templates.format_schema_info(schema_info)
            formatted_examples = self._get_relevant_examples(question, examples or [])
            
            prompt = self.prompt_templates.get_sql_prompt().format(
                question=question,
                schema_info=formatted_schema,
                examples=formatted_examples
            )
            
            # 5. 토큰 사용량 확인
            token_count = len(self.token_encoder.encode(prompt))
            if token_count > settings.openai_max_tokens * 0.8:  # 80% 임계값
                logger.warning(f"높은 토큰 사용량: {token_count}")
            
            # 6. LLM 호출
            response = await self._call_llm_with_fallback(prompt)
            
            # 7. 응답 파싱
            result_data = self._parse_json_response(response)
            
            # 8. SQL 보안 검증
            sql_validation = self.sql_validator.validate_sql(
                result_data.get('sql', ''),
                context=user_context
            )
            
            if not sql_validation.is_safe:
                raise SecurityError(f"안전하지 않은 SQL: {sql_validation.violations}")
            
            # 9. 결과 생성
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            result = SQLGenerationResult(
                sql=sql_validation.sanitized_sql or result_data.get('sql', ''),
                explanation=result_data.get('explanation', ''),
                estimated_rows=result_data.get('estimated_rows', 0),
                confidence=result_data.get('confidence', 0.0),
                warnings=result_data.get('warnings', []) + sql_validation.warnings or [],
                tables_used=result_data.get('tables_used', []),
                requires_join=result_data.get('requires_join', False),
                complexity=result_data.get('complexity', 'medium'),
                processing_time_ms=processing_time
            )
            
            # 10. 캐시 저장
            await self._cache_result(cache_key, result)
            
            # 11. 메트릭 업데이트
            self._update_metrics(True, token_count, result.confidence)
            
            logger.info(
                "SQL 생성 성공",
                extra={
                    "confidence": result.confidence,
                    "complexity": result.complexity,
                    "processing_time_ms": processing_time,
                    "tables_used": len(result.tables_used)
                }
            )
            
            return result
            
        except Exception as e:
            self._update_metrics(False, 0, 0.0)
            logger.error(
                "SQL 생성 실패",
                extra={
                    "error": str(e),
                    "question_hash": hashlib.sha256(question.encode()).hexdigest()[:16]
                }
            )
            raise LLMProcessingError(f"SQL 쿼리 생성에 실패했습니다: {str(e)}")
    
    async def generate_excel_analysis(
        self,
        question: str,
        dataframe_info: Dict[str, Any],
        sample_data: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> ExcelAnalysisResult:
        """
        자연어 질문을 Excel 분석 코드로 변환
        
        Args:
            question: 사용자 질문
            dataframe_info: 데이터프레임 정보
            sample_data: 샘플 데이터
            user_context: 사용자 컨텍스트 정보
            
        Returns:
            ExcelAnalysisResult: Excel 분석 결과
        """
        start_time = datetime.now()
        
        try:
            # 1. 입력 검증
            self._validate_input(question)
            
            # 2. 프롬프트 인젝션 검사
            if self.injection_detector.detect_injection(question):
                raise SecurityError("프롬프트 인젝션 시도가 감지되었습니다")
            
            # 3. 캐시 확인
            cache_key = self._generate_cache_key("excel", question, dataframe_info)
            cached_result = await self._get_cached_result(cache_key)
            if cached_result:
                self.metrics['cache_hits'] += 1
                return cached_result
            
            # 4. 프롬프트 구성
            formatted_df_info = self.prompt_templates.format_dataframe_info(dataframe_info)
            
            prompt = self.prompt_templates.get_excel_prompt().format(
                question=question,
                dataframe_info=formatted_df_info,
                sample_data=sample_data or "샘플 데이터 없음"
            )
            
            # 5. LLM 호출
            response = await self._call_llm_with_fallback(prompt)
            
            # 6. 응답 파싱
            result_data = self._parse_json_response(response)
            
            # 7. Python 코드 안전성 검증
            generated_code = result_data.get('code', '')
            if not self._validate_python_code(generated_code):
                raise SecurityError("안전하지 않은 Python 코드가 생성되었습니다")
            
            # 8. 결과 생성
            processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            result = ExcelAnalysisResult(
                code=generated_code,
                explanation=result_data.get('explanation', ''),
                expected_output=result_data.get('expected_output', ''),
                confidence=result_data.get('confidence', 0.0),
                safety_check=result_data.get('safety_check', 'needs_review'),
                visualization_type=result_data.get('visualization_type', 'none'),
                complexity=result_data.get('complexity', 'medium'),
                processing_time_ms=processing_time
            )
            
            # 9. 캐시 저장
            await self._cache_result(cache_key, result)
            
            # 10. 메트릭 업데이트
            token_count = len(self.token_encoder.encode(prompt))
            self._update_metrics(True, token_count, result.confidence)
            
            logger.info(
                "Excel 분석 생성 성공",
                extra={
                    "confidence": result.confidence,
                    "complexity": result.complexity,
                    "processing_time_ms": processing_time,
                    "visualization_type": result.visualization_type
                }
            )
            
            return result
            
        except Exception as e:
            self._update_metrics(False, 0, 0.0)
            logger.error(
                "Excel 분석 생성 실패",
                extra={
                    "error": str(e),
                    "question_hash": hashlib.sha256(question.encode()).hexdigest()[:16]
                }
            )
            raise LLMProcessingError(f"Excel 분석 코드 생성에 실패했습니다: {str(e)}")
    
    async def classify_question(self, question: str) -> QuestionClassificationResult:
        """
        질문을 분석하여 적절한 분석 유형 결정
        
        Args:
            question: 사용자 질문
            
        Returns:
            QuestionClassificationResult: 질문 분류 결과
        """
        try:
            # 입력 검증
            self._validate_input(question)
            
            # 프롬프트 구성
            prompt = self.prompt_templates.get_classification_prompt().format(
                question=question
            )
            
            # LLM 호출
            response = await self._call_llm_with_fallback(prompt)
            result_data = self._parse_json_response(response)
            
            return QuestionClassificationResult(
                analysis_type=result_data.get('analysis_type', 'general'),
                confidence=result_data.get('confidence', 0.0),
                reasoning=result_data.get('reasoning', ''),
                keywords=result_data.get('keywords', []),
                requires_data_connection=result_data.get('requires_data_connection', False),
                complexity=result_data.get('complexity', 'medium'),
                estimated_processing_time=result_data.get('estimated_processing_time', 'medium')
            )
            
        except Exception as e:
            logger.error(f"질문 분류 실패: {str(e)}")
            # 기본값 반환
            return QuestionClassificationResult(
                analysis_type='general',
                confidence=0.5,
                reasoning='분류 실패로 기본값 사용',
                keywords=[],
                requires_data_connection=False,
                complexity='medium',
                estimated_processing_time='medium'
            )
    
    def _validate_input(self, question: str):
        """입력 검증"""
        if not question or not question.strip():
            raise ValueError("질문이 비어있습니다")
        
        if len(question) > 1000:
            raise ValueError("질문이 너무 깁니다 (최대 1000자)")
    
    def _validate_python_code(self, code: str) -> bool:
        """Python 코드 안전성 검증"""
        import ast
        import re
        
        # 금지된 패턴 검사
        forbidden_patterns = [
            r'import\s+(os|sys|subprocess|shutil)',
            r'exec\s*\(',
            r'eval\s*\(',
            r'open\s*\(',
            r'__import__',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False
        
        try:
            # 구문 검사
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    async def _call_llm_with_fallback(self, prompt: str) -> str:
        """LLM 호출 (폴백 포함)"""
        try:
            message = HumanMessage(content=prompt)
            response = await self.llm.ainvoke([message])
            return response.content
        except Exception as e:
            logger.warning(f"주 모델 실패, 폴백 모델 사용: {str(e)}")
            try:
                message = HumanMessage(content=prompt)
                response = await self.fallback_llm.ainvoke([message])
                return response.content
            except Exception as fallback_error:
                raise LLMProcessingError(f"LLM 호출 실패: {str(fallback_error)}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """JSON 응답 파싱"""
        try:
            # JSON 블록 추출
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                raise ValueError("JSON 형식을 찾을 수 없습니다")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}, 응답: {response[:200]}")
            raise ValueError("LLM 응답을 파싱할 수 없습니다")
    
    def _generate_cache_key(self, operation: str, question: str, context: Dict) -> str:
        """캐시 키 생성"""
        context_str = json.dumps(context, sort_keys=True)
        content = f"{operation}:{question}:{context_str}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    async def _get_cached_result(self, cache_key: str) -> Optional[Any]:
        """캐시에서 결과 조회"""
        if not self.cache_client:
            return None
        
        try:
            cached_data = await self.cache_client.get(f"datagenie:llm:{cache_key}")
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            logger.warning(f"캐시 조회 실패: {str(e)}")
        
        return None
    
    async def _cache_result(self, cache_key: str, result: Any):
        """결과를 캐시에 저장"""
        if not self.cache_client:
            return
        
        try:
            # dataclass를 dict로 변환
            if hasattr(result, '__dict__'):
                result_dict = result.__dict__
            else:
                result_dict = result
            
            await self.cache_client.setex(
                f"datagenie:llm:{cache_key}",
                3600,  # 1시간 TTL
                json.dumps(result_dict, ensure_ascii=False)
            )
        except Exception as e:
            logger.warning(f"캐시 저장 실패: {str(e)}")
    
    def _get_relevant_examples(self, question: str, examples: List[Dict[str, str]]) -> str:
        """관련성 높은 예시 선택"""
        if not examples:
            return "예시 없음"
        
        # 간단한 키워드 매칭으로 관련 예시 선택
        question_words = set(question.lower().split())
        scored_examples = []
        
        for example in examples:
            example_words = set(example.get('question', '').lower().split())
            relevance_score = len(question_words & example_words)
            scored_examples.append((relevance_score, example))
        
        # 관련성 순으로 정렬하여 상위 3개 선택
        scored_examples.sort(key=lambda x: x[0], reverse=True)
        top_examples = [ex[1] for ex in scored_examples[:3]]
        
        return self.prompt_templates.format_examples(top_examples)
    
    def _update_metrics(self, success: bool, tokens_used: int, confidence: float):
        """메트릭 업데이트"""
        self.metrics['total_requests'] += 1
        if success:
            self.metrics['successful_requests'] += 1
        self.metrics['total_tokens_used'] += tokens_used
        
        # 평균 신뢰도 계산
        if success and confidence > 0:
            current_avg = self.metrics['average_confidence']
            total_success = self.metrics['successful_requests']
            self.metrics['average_confidence'] = (
                (current_avg * (total_success - 1) + confidence) / total_success
            )
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """성능 메트릭 반환"""
        total_requests = self.metrics['total_requests']
        if total_requests == 0:
            return {}
        
        return {
            'success_rate': self.metrics['successful_requests'] / total_requests,
            'cache_hit_rate': self.metrics['cache_hits'] / total_requests,
            'total_tokens_used': self.metrics['total_tokens_used'],
            'average_confidence': self.metrics['average_confidence'],
            'total_requests': total_requests
        }


class LLMProcessingError(Exception):
    """LLM 처리 관련 예외"""
    pass


class SecurityError(Exception):
    """보안 관련 예외"""
    pass
