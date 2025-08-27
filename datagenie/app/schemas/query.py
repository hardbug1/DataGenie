"""
Query Pydantic Schemas

쿼리 실행 관련 API 요청/응답 스키마를 정의합니다.
Clean Architecture: Interface Layer
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


class QueryType(str, Enum):
    """쿼리 타입"""
    NATURAL_LANGUAGE = "natural_language"
    SQL = "sql"
    EXCEL_ANALYSIS = "excel_analysis"


class QueryExecutionStatus(str, Enum):
    """쿼리 실행 상태"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VisualizationType(str, Enum):
    """시각화 타입"""
    TABLE = "table"
    BAR_CHART = "bar_chart"
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    HISTOGRAM = "histogram"


class QueryRequest(BaseModel):
    """쿼리 실행 요청 스키마"""
    
    question: str = Field(..., min_length=1, max_length=1000, description="자연어 질문 또는 SQL 쿼리")
    query_type: QueryType = Field(default=QueryType.NATURAL_LANGUAGE, description="쿼리 타입")
    connection_id: str = Field(..., description="데이터베이스 연결 ID")
    
    # 실행 옵션
    limit: Optional[int] = Field(default=100, ge=1, le=10000, description="결과 행 수 제한")
    timeout_seconds: Optional[int] = Field(default=30, ge=1, le=300, description="실행 타임아웃 (초)")
    
    # 시각화 옵션
    auto_visualize: bool = Field(default=True, description="자동 시각화 생성 여부")
    preferred_chart_type: Optional[VisualizationType] = Field(None, description="선호하는 차트 타입")
    
    # 분석 옵션
    include_summary: bool = Field(default=True, description="결과 요약 포함 여부")
    include_insights: bool = Field(default=True, description="인사이트 분석 포함 여부")
    
    @validator('question')
    def validate_question(cls, v):
        """질문 내용 검증"""
        v = v.strip()
        if not v:
            raise ValueError('질문이 비어있습니다')
        
        # 보안 키워드 검사
        dangerous_keywords = ['drop', 'delete', 'truncate', 'alter', 'create', 'insert', 'update']
        v_lower = v.lower()
        for keyword in dangerous_keywords:
            if keyword in v_lower:
                raise ValueError(f'보안상 {keyword.upper()} 명령어는 사용할 수 없습니다')
        
        return v


class QueryResultData(BaseModel):
    """쿼리 결과 데이터 스키마"""
    
    columns: List[str] = Field(..., description="컬럼 이름 목록")
    rows: List[List[Any]] = Field(..., description="데이터 행 목록")
    total_rows: int = Field(..., description="총 행 수")
    execution_time_ms: int = Field(..., description="실행 시간 (밀리초)")


class QueryVisualization(BaseModel):
    """쿼리 시각화 스키마"""
    
    chart_type: VisualizationType = Field(..., description="차트 타입")
    chart_data: Dict[str, Any] = Field(..., description="차트 데이터 (Plotly JSON)")
    title: str = Field(..., description="차트 제목")
    description: Optional[str] = Field(None, description="차트 설명")


class QueryInsights(BaseModel):
    """쿼리 인사이트 스키마"""
    
    summary: str = Field(..., description="결과 요약")
    key_findings: List[str] = Field(default_factory=list, description="주요 발견사항")
    recommendations: List[str] = Field(default_factory=list, description="권장사항")
    data_quality_notes: List[str] = Field(default_factory=list, description="데이터 품질 참고사항")


class QueryResponse(BaseModel):
    """쿼리 실행 응답 스키마"""
    
    query_id: str = Field(..., description="쿼리 실행 ID")
    status: QueryExecutionStatus = Field(..., description="실행 상태")
    
    # 실행 정보
    executed_sql: Optional[str] = Field(None, description="실행된 SQL 쿼리")
    execution_time_ms: Optional[int] = Field(None, description="실행 시간 (밀리초)")
    
    # 결과 데이터
    data: Optional[QueryResultData] = Field(None, description="쿼리 결과 데이터")
    
    # 시각화
    visualizations: List[QueryVisualization] = Field(default_factory=list, description="생성된 시각화 목록")
    
    # 분석 결과
    insights: Optional[QueryInsights] = Field(None, description="인사이트 분석 결과")
    
    # 오류 정보
    error_message: Optional[str] = Field(None, description="오류 메시지")
    error_code: Optional[str] = Field(None, description="오류 코드")
    
    # 메타데이터
    created_at: datetime = Field(..., description="생성 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")


class QueryHistory(BaseModel):
    """쿼리 실행 이력 스키마"""
    
    id: str = Field(..., description="쿼리 ID")
    user_id: str = Field(..., description="사용자 ID")
    connection_id: str = Field(..., description="데이터베이스 연결 ID")
    
    # 쿼리 정보
    original_question: str = Field(..., description="원본 질문")
    query_type: QueryType = Field(..., description="쿼리 타입")
    executed_sql: Optional[str] = Field(None, description="실행된 SQL")
    
    # 실행 결과
    status: QueryExecutionStatus = Field(..., description="실행 상태")
    execution_time_ms: Optional[int] = Field(None, description="실행 시간 (밀리초)")
    result_rows: Optional[int] = Field(None, description="결과 행 수")
    
    # 시간 정보
    created_at: datetime = Field(..., description="생성 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")
    
    # 메타데이터
    has_visualizations: bool = Field(default=False, description="시각화 포함 여부")
    has_insights: bool = Field(default=False, description="인사이트 포함 여부")
    
    class Config:
        from_attributes = True


class QueryExecutionRequest(BaseModel):
    """쿼리 실행 상태 업데이트 요청 스키마"""
    
    status: QueryExecutionStatus = Field(..., description="새로운 실행 상태")
    error_message: Optional[str] = Field(None, description="오류 메시지")
    execution_time_ms: Optional[int] = Field(None, description="실행 시간 (밀리초)")
    result_summary: Optional[Dict[str, Any]] = Field(None, description="결과 요약")
