"""
Database Connection Pydantic Schemas

데이터베이스 연결 관련 API 요청/응답 스키마를 정의합니다.
Clean Architecture: Interface Layer
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class DatabaseType(str, Enum):
    """지원하는 데이터베이스 타입"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    ORACLE = "oracle"
    MSSQL = "mssql"


class ConnectionStatus(str, Enum):
    """연결 상태"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    TESTING = "testing"


class DatabaseConnectionBase(BaseModel):
    """데이터베이스 연결 기본 스키마"""
    
    name: str = Field(..., min_length=1, max_length=100, description="연결 이름")
    description: Optional[str] = Field(None, max_length=500, description="연결 설명")
    database_type: DatabaseType = Field(..., description="데이터베이스 타입")
    host: str = Field(..., description="데이터베이스 호스트")
    port: int = Field(..., ge=1, le=65535, description="데이터베이스 포트")
    database_name: str = Field(..., description="데이터베이스 이름")
    username: str = Field(..., description="사용자명")
    is_read_only: bool = Field(default=True, description="읽기 전용 연결 여부")


class DatabaseConnectionCreate(DatabaseConnectionBase):
    """데이터베이스 연결 생성 요청 스키마"""
    
    password: str = Field(..., description="비밀번호")
    connection_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="추가 연결 옵션")
    
    @validator('is_read_only')
    def validate_read_only(cls, v):
        """보안상 읽기 전용 연결만 허용"""
        if not v:
            raise ValueError('보안상 읽기 전용 연결만 허용됩니다')
        return v


class DatabaseConnectionUpdate(BaseModel):
    """데이터베이스 연결 수정 요청 스키마"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="연결 이름")
    description: Optional[str] = Field(None, max_length=500, description="연결 설명")
    host: Optional[str] = Field(None, description="데이터베이스 호스트")
    port: Optional[int] = Field(None, ge=1, le=65535, description="데이터베이스 포트")
    database_name: Optional[str] = Field(None, description="데이터베이스 이름")
    username: Optional[str] = Field(None, description="사용자명")
    password: Optional[str] = Field(None, description="비밀번호")
    connection_options: Optional[Dict[str, Any]] = Field(None, description="추가 연결 옵션")
    is_active: Optional[bool] = Field(None, description="연결 활성화 상태")


class DatabaseConnectionTest(BaseModel):
    """데이터베이스 연결 테스트 요청 스키마"""
    
    database_type: DatabaseType = Field(..., description="데이터베이스 타입")
    host: str = Field(..., description="데이터베이스 호스트")
    port: int = Field(..., ge=1, le=65535, description="데이터베이스 포트")
    database_name: str = Field(..., description="데이터베이스 이름")
    username: str = Field(..., description="사용자명")
    password: str = Field(..., description="비밀번호")
    connection_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="추가 연결 옵션")


class DatabaseConnectionResponse(DatabaseConnectionBase):
    """데이터베이스 연결 응답 스키마"""
    
    id: str = Field(..., description="연결 ID")
    user_id: str = Field(..., description="소유자 사용자 ID")
    status: ConnectionStatus = Field(..., description="연결 상태")
    created_at: datetime = Field(..., description="생성 시간")
    updated_at: datetime = Field(..., description="수정 시간")
    last_tested_at: Optional[datetime] = Field(None, description="마지막 테스트 시간")
    last_used_at: Optional[datetime] = Field(None, description="마지막 사용 시간")
    
    # 통계 정보
    total_queries: int = Field(default=0, description="총 쿼리 실행 횟수")
    successful_queries: int = Field(default=0, description="성공한 쿼리 횟수")
    
    class Config:
        from_attributes = True


class DatabaseConnectionTestResult(BaseModel):
    """데이터베이스 연결 테스트 결과 스키마"""
    
    success: bool = Field(..., description="테스트 성공 여부")
    message: str = Field(..., description="테스트 결과 메시지")
    response_time_ms: Optional[int] = Field(None, description="응답 시간 (밀리초)")
    database_version: Optional[str] = Field(None, description="데이터베이스 버전")
    schema_count: Optional[int] = Field(None, description="스키마 개수")
    table_count: Optional[int] = Field(None, description="테이블 개수")
