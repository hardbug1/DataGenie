"""
Analysis Pydantic Schemas

Clean Architecture: Interface Adapters
API 요청/응답을 위한 데이터 검증 스키마
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime


class AnalysisRequestSchema(BaseModel):
    """분석 요청 스키마"""
    
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="분석할 자연어 질문",
        example="지난 3개월 매출 추이를 보여주세요"
    )
    
    connection_id: Optional[str] = Field(
        None,
        description="데이터베이스 연결 ID",
        example="uuid-connection-id"
    )
    
    options: Optional[Dict[str, Any]] = Field(
        None,
        description="추가 분석 옵션",
        example={"auto_visualize": True, "include_insights": True}
    )
    
    @validator('question')
    def validate_question(cls, v):
        """질문 유효성 검증"""
        if not v or not v.strip():
            raise ValueError('질문은 비어있을 수 없습니다')
        
        # 금지된 키워드 검사
        forbidden_keywords = ['drop', 'delete', 'truncate', 'alter']
        question_lower = v.lower()
        
        for keyword in forbidden_keywords:
            if keyword in question_lower:
                raise ValueError(f'금지된 키워드가 포함되어 있습니다: {keyword}')
        
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "지난 3개월 매출 추이를 보여주세요",
                "connection_id": "uuid-connection-id",
                "options": {
                    "auto_visualize": True,
                    "include_insights": True
                }
            }
        }


class AnalysisResultSchema(BaseModel):
    """분석 결과 스키마"""
    
    analysis_type: str = Field(..., description="분석 유형")
    question: str = Field(..., description="원본 질문")
    sql_query: Optional[str] = Field(None, description="생성된 SQL 쿼리")
    generated_code: Optional[str] = Field(None, description="생성된 분석 코드")
    execution_success: bool = Field(True, description="실행 성공 여부")
    
    data: Optional[List[Dict[str, Any]]] = Field(None, description="결과 데이터")
    columns: Optional[List[str]] = Field(None, description="컬럼 목록")
    row_count: Optional[int] = Field(None, description="결과 행 수")
    
    chart_type: Optional[str] = Field(None, description="차트 유형")
    chart_config: Optional[Dict[str, Any]] = Field(None, description="차트 설정")
    chart_data: Optional[str] = Field(None, description="차트 데이터 (JSON)")
    
    summary: Optional[str] = Field(None, description="결과 요약")
    insights: Optional[List[str]] = Field(None, description="인사이트 목록")
    recommendations: Optional[List[str]] = Field(None, description="추천 사항")
    
    metadata: Optional[Dict[str, Any]] = Field(None, description="메타데이터")


class AnalysisResponseSchema(BaseModel):
    """분석 응답 스키마"""
    
    success: bool = Field(..., description="요청 성공 여부")
    data: Optional[Dict[str, Any]] = Field(None, description="응답 데이터")
    message: str = Field(..., description="응답 메시지")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="응답 시간")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "query_id": "uuid-query-id",
                    "question": "지난 3개월 매출 추이를 보여주세요",
                    "query_type": "database",
                    "status": "completed",
                    "result": {
                        "analysis_type": "database",
                        "data": [
                            {"month": "2024-01", "sales": 1000000},
                            {"month": "2024-02", "sales": 1200000}
                        ],
                        "chart_type": "line",
                        "summary": "매출이 지속적으로 증가하고 있습니다."
                    },
                    "execution_time_ms": 1250
                },
                "message": "분석이 성공적으로 완료되었습니다.",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ErrorResponseSchema(BaseModel):
    """오류 응답 스키마"""
    
    success: bool = Field(False, description="요청 성공 여부")
    error: Dict[str, Any] = Field(..., description="오류 정보")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="응답 시간")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": "INVALID_QUERY",
                    "message": "질문이 유효하지 않습니다",
                    "details": {
                        "field": "question",
                        "reason": "질문이 비어있습니다"
                    }
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class QuestionAnalysisSchema(BaseModel):
    """질문 분석 스키마"""
    
    type: str = Field(..., description="질문 유형")
    intent: str = Field(..., description="사용자 의도")
    entities: Dict[str, Any] = Field(..., description="추출된 엔티티")
    confidence: float = Field(..., ge=0.0, le=1.0, description="신뢰도")
    suggested_tables: List[str] = Field(default_factory=list, description="추천 테이블")
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "DB_QUERY",
                "intent": "매출 데이터 조회 및 시각화",
                "entities": {
                    "time_period": "지난 3개월",
                    "metric": "매출",
                    "visualization": "추이"
                },
                "confidence": 0.95,
                "suggested_tables": ["orders", "products"]
            }
        }
