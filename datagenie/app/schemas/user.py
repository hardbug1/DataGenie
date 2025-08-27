"""
User Pydantic Schemas

사용자 관련 API 요청/응답 스키마를 정의합니다.
Clean Architecture: Interface Layer
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    
    email: EmailStr = Field(..., description="사용자 이메일")
    full_name: str = Field(..., min_length=2, max_length=100, description="사용자 전체 이름")
    is_active: bool = Field(default=True, description="계정 활성화 상태")


class UserCreate(UserBase):
    """사용자 생성 요청 스키마"""
    
    password: str = Field(..., min_length=8, max_length=128, description="비밀번호")
    
    @validator('password')
    def validate_password(cls, v):
        """비밀번호 복잡성 검증"""
        if not any(c.isupper() for c in v):
            raise ValueError('비밀번호는 최소 하나의 대문자를 포함해야 합니다')
        if not any(c.islower() for c in v):
            raise ValueError('비밀번호는 최소 하나의 소문자를 포함해야 합니다')
        if not any(c.isdigit() for c in v):
            raise ValueError('비밀번호는 최소 하나의 숫자를 포함해야 합니다')
        return v


class UserUpdate(BaseModel):
    """사용자 정보 수정 요청 스키마"""
    
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="사용자 전체 이름")
    email: Optional[EmailStr] = Field(None, description="사용자 이메일")
    is_active: Optional[bool] = Field(None, description="계정 활성화 상태")


class UserLogin(BaseModel):
    """사용자 로그인 요청 스키마"""
    
    email: EmailStr = Field(..., description="사용자 이메일")
    password: str = Field(..., description="비밀번호")


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    
    id: str = Field(..., description="사용자 ID")
    created_at: datetime = Field(..., description="계정 생성 시간")
    updated_at: datetime = Field(..., description="계정 수정 시간")
    last_login_at: Optional[datetime] = Field(None, description="마지막 로그인 시간")
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """사용자 프로필 스키마"""
    
    id: str = Field(..., description="사용자 ID")
    email: EmailStr = Field(..., description="사용자 이메일")
    full_name: str = Field(..., description="사용자 전체 이름")
    is_active: bool = Field(..., description="계정 활성화 상태")
    created_at: datetime = Field(..., description="계정 생성 시간")
    last_login_at: Optional[datetime] = Field(None, description="마지막 로그인 시간")
    
    # 통계 정보
    total_queries: int = Field(default=0, description="총 쿼리 실행 횟수")
    successful_queries: int = Field(default=0, description="성공한 쿼리 횟수")
    
    class Config:
        from_attributes = True
