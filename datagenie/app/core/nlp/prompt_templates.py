"""
DataGenie LLM Prompt Templates

Clean Architecture: Application Core
LLM 프롬프트 엔지니어링 및 템플릿 관리
"""

from typing import Dict, List, Any, Optional
from langchain.prompts import PromptTemplate
import structlog

logger = structlog.get_logger(__name__)


class DataGeniePromptTemplates:
    """
    DataGenie 전용 프롬프트 템플릿 관리자
    
    LLM Integration 규칙 준수:
    - 정확성과 보안을 최우선으로 설계
    - 프롬프트 인젝션 방지
    - 구조화된 JSON 응답 형식
    """
    
    # SQL 생성 프롬프트 (MANDATORY)
    SQL_GENERATION_PROMPT = PromptTemplate(
        input_variables=["question", "schema_info", "examples"],
        template="""당신은 DataGenie의 전문 SQL 분석가입니다.

중요 규칙:
- SELECT 쿼리만 생성 (INSERT/UPDATE/DELETE/DROP 금지)
- 매개변수화된 쿼리로 SQL 인젝션 방지
- 결과를 최대 1000행으로 제한
- PostgreSQL/MySQL 호환 문법 사용
- 개인정보 자동 마스킹 고려
- 적절한 에러 처리 포함

데이터베이스 스키마:
{schema_info}

예시 쿼리:
{examples}

사용자 질문: {question}

응답 형식 (JSON):
{{
    "sql": "SELECT 컬럼1, 컬럼2 FROM 테이블 WHERE 조건 LIMIT 1000",
    "explanation": "쿼리가 수행하는 작업에 대한 간단한 설명",
    "estimated_rows": 150,
    "confidence": 0.95,
    "warnings": ["잠재적 문제나 제한사항"],
    "tables_used": ["테이블1", "테이블2"],
    "requires_join": false,
    "complexity": "simple|medium|complex"
}}

SQL 쿼리:"""
    )
    
    # Excel 분석 프롬프트 (MANDATORY)
    EXCEL_ANALYSIS_PROMPT = PromptTemplate(
        input_variables=["question", "dataframe_info", "sample_data"],
        template="""당신은 DataGenie의 전문 Python 데이터 분석가입니다.

중요 규칙:
- 안전한 pandas 연산만 생성
- 파일 시스템 접근 금지 (open(), read_csv() 경로 사용 금지)
- 네트워크 요청 금지 (requests, urllib 금지)
- 서브프로세스나 시스템 호출 금지
- 제공된 'df' 데이터프레임만 사용
- 적절한 에러 처리 포함
- 결과를 최대 1000행으로 제한

데이터프레임 정보:
{dataframe_info}

샘플 데이터:
{sample_data}

사용자 질문: {question}

응답 형식 (JSON):
{{
    "code": "# Python pandas 코드\\ntry:\\n    result = df.head(10)\\nexcept Exception as e:\\n    print(f'Error: {{e}}')",
    "explanation": "분석이 수행하는 작업에 대한 설명",
    "expected_output": "예상 결과에 대한 설명",
    "confidence": 0.92,
    "safety_check": "confirmed_safe",
    "visualization_type": "bar_chart|line_chart|scatter|table|none",
    "complexity": "simple|medium|complex"
}}

Python 코드:"""
    )
    
    # 질문 분류 프롬프트
    QUESTION_CLASSIFICATION_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""당신은 DataGenie의 질문 분류 전문가입니다.

사용자 질문을 분석하여 적절한 분석 유형을 결정해주세요.

사용자 질문: {question}

응답 형식 (JSON):
{{
    "analysis_type": "database|excel|general",
    "confidence": 0.95,
    "reasoning": "분류 근거",
    "keywords": ["키워드1", "키워드2"],
    "requires_data_connection": true,
    "complexity": "simple|medium|complex",
    "estimated_processing_time": "fast|medium|slow"
}}

분류 결과:"""
    )
    
    # 스키마 요약 프롬프트
    SCHEMA_SUMMARY_PROMPT = PromptTemplate(
        input_variables=["schema_info", "question"],
        template="""당신은 DataGenie의 데이터베이스 스키마 전문가입니다.

주어진 질문에 가장 관련성이 높은 테이블과 컬럼을 식별해주세요.

데이터베이스 스키마:
{schema_info}

사용자 질문: {question}

응답 형식 (JSON):
{{
    "relevant_tables": ["테이블1", "테이블2"],
    "relevant_columns": {{
        "테이블1": ["컬럼1", "컬럼2"],
        "테이블2": ["컬럼3", "컬럼4"]
    }},
    "join_requirements": [
        {{"from": "테이블1", "to": "테이블2", "on": "컬럼"}}
    ],
    "confidence": 0.90,
    "complexity_assessment": "simple|medium|complex"
}}

스키마 분석:"""
    )
    
    # 시각화 추천 프롬프트
    VISUALIZATION_RECOMMENDATION_PROMPT = PromptTemplate(
        input_variables=["question", "data_summary"],
        template="""당신은 DataGenie의 데이터 시각화 전문가입니다.

질문과 데이터 특성을 분석하여 최적의 시각화 방법을 추천해주세요.

사용자 질문: {question}

데이터 요약:
{data_summary}

응답 형식 (JSON):
{{
    "recommended_chart": "bar|line|scatter|pie|heatmap|table",
    "chart_config": {{
        "x_axis": "컬럼명",
        "y_axis": "컬럼명",
        "color_by": "컬럼명",
        "title": "차트 제목"
    }},
    "alternative_charts": ["bar", "line"],
    "confidence": 0.88,
    "reasoning": "추천 근거"
}}

시각화 추천:"""
    )
    
    @classmethod
    def get_sql_prompt(cls) -> PromptTemplate:
        """SQL 생성 프롬프트 반환"""
        return cls.SQL_GENERATION_PROMPT
    
    @classmethod
    def get_excel_prompt(cls) -> PromptTemplate:
        """Excel 분석 프롬프트 반환"""
        return cls.EXCEL_ANALYSIS_PROMPT
    
    @classmethod
    def get_classification_prompt(cls) -> PromptTemplate:
        """질문 분류 프롬프트 반환"""
        return cls.QUESTION_CLASSIFICATION_PROMPT
    
    @classmethod
    def get_schema_summary_prompt(cls) -> PromptTemplate:
        """스키마 요약 프롬프트 반환"""
        return cls.SCHEMA_SUMMARY_PROMPT
    
    @classmethod
    def get_visualization_prompt(cls) -> PromptTemplate:
        """시각화 추천 프롬프트 반환"""
        return cls.VISUALIZATION_RECOMMENDATION_PROMPT
    
    @classmethod
    def format_schema_info(cls, schema: Dict[str, Any]) -> str:
        """스키마 정보를 프롬프트용으로 포맷팅"""
        formatted_tables = []
        
        for table_name, table_info in schema.items():
            columns = []
            for col in table_info.get('columns', []):
                col_desc = f"{col['name']} ({col['type']})"
                if col.get('primary_key'):
                    col_desc += " [PK]"
                if col.get('foreign_key'):
                    col_desc += f" [FK -> {col['foreign_key']}]"
                if not col.get('nullable', True):
                    col_desc += " [NOT NULL]"
                columns.append(col_desc)
            
            # 테이블당 최대 15개 컬럼만 표시 (토큰 최적화)
            if len(columns) > 15:
                columns = columns[:15] + ["... (더 많은 컬럼 있음)"]
            
            table_desc = f"테이블 '{table_name}':\n  - " + "\n  - ".join(columns)
            formatted_tables.append(table_desc)
        
        return "\n\n".join(formatted_tables)
    
    @classmethod
    def format_examples(cls, examples: List[Dict[str, str]]) -> str:
        """예시 쿼리를 프롬프트용으로 포맷팅"""
        formatted_examples = []
        
        for i, example in enumerate(examples[:3], 1):  # 최대 3개 예시
            formatted_example = f"예시 {i}:\n질문: {example['question']}\nSQL: {example['sql']}"
            formatted_examples.append(formatted_example)
        
        return "\n\n".join(formatted_examples)
    
    @classmethod
    def format_dataframe_info(cls, df_info: Dict[str, Any]) -> str:
        """데이터프레임 정보를 프롬프트용으로 포맷팅"""
        info_parts = []
        
        # 기본 정보
        info_parts.append(f"행 수: {df_info.get('row_count', 'Unknown')}")
        info_parts.append(f"열 수: {df_info.get('column_count', 'Unknown')}")
        
        # 컬럼 정보
        if 'columns' in df_info:
            columns_info = []
            for col_name, col_info in df_info['columns'].items():
                col_desc = f"{col_name} ({col_info.get('dtype', 'unknown')})"
                if col_info.get('null_count', 0) > 0:
                    col_desc += f" [결측값: {col_info['null_count']}개]"
                columns_info.append(col_desc)
            
            info_parts.append("컬럼 정보:")
            info_parts.extend([f"  - {col}" for col in columns_info])
        
        return "\n".join(info_parts)


class PromptInjectionDetector:
    """
    프롬프트 인젝션 탐지기
    
    LLM Integration 규칙 준수:
    - 모든 사용자 입력에 대한 보안 검사
    - 프롬프트 인젝션 패턴 탐지
    """
    
    INJECTION_PATTERNS = [
        r'이전\s*지시사항을?\s*무시',
        r'위의?\s*모든?\s*것을?\s*잊어',
        r'새로운?\s*지시사항?:',
        r'시스템\s*:',
        r'어시스턴트\s*:',
        r'사용자\s*:',
        r'중요\s*규칙?:',
        r'응답\s*형식',
        r'```.*?```',  # 입력의 코드 블록
        r'<\|.*?\|>',  # 특수 토큰
        r'CRITICAL\s+RULES?:',
        r'RESPONSE\s+FORMAT',
        r'ignore\s+previous\s+instructions',
        r'forget\s+everything\s+above',
    ]
    
    def __init__(self):
        """프롬프트 인젝션 탐지기 초기화"""
        import re
        self._compiled_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self.INJECTION_PATTERNS
        ]
    
    def detect_injection(self, user_input: str) -> bool:
        """
        사용자 입력에서 프롬프트 인젝션 탐지
        
        Args:
            user_input: 검사할 사용자 입력
            
        Returns:
            bool: 인젝션 시도 감지 여부
        """
        if not user_input or not isinstance(user_input, str):
            return False
        
        for pattern in self._compiled_patterns:
            if pattern.search(user_input):
                logger.warning(
                    "프롬프트 인젝션 시도 감지",
                    extra={
                        "input_hash": hash(user_input) % 10000,  # 간단한 해시
                        "pattern_matched": True
                    }
                )
                return True
        
        return False
    
    def sanitize_input(self, user_input: str) -> str:
        """
        사용자 입력 정화
        
        Args:
            user_input: 정화할 입력
            
        Returns:
            str: 정화된 입력
        """
        if self.detect_injection(user_input):
            raise ValueError("프롬프트 인젝션 시도가 감지되었습니다")
        
        # 기본적인 정화 (특수 문자 제거 등)
        sanitized = user_input.strip()
        
        # 연속된 공백 정리
        import re
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized
