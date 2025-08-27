"""
Authentication Pydantic Schemas

Clean Architecture: Interface Layer
인증 관련 API 요청/응답 스키마를 정의합니다.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

from app.schemas.common import BaseResponse


class LoginRequest(BaseModel):
    """로그인 요청 스키마"""
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="사용자명"
    )
    
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="비밀번호"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class RefreshTokenRequest(BaseModel):
    """토큰 갱신 요청 스키마"""
    
    refresh_token: str = Field(
        ...,
        description="리프레시 토큰"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class UserInfoResponse(BaseModel):
    """사용자 정보 응답 스키마"""
    
    user_id: str = Field(..., description="사용자 ID")
    username: str = Field(..., description="사용자명")
    email: str = Field(..., description="이메일")
    role: str = Field(..., description="역할")
    permissions: List[str] = Field(default_factory=list, description="권한 목록")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-123",
                "username": "admin",
                "email": "admin@datagenie.com",
                "role": "admin",
                "permissions": [
                    "analysis:execute",
                    "query:read",
                    "user:manage"
                ]
            }
        }


class TokenResponse(BaseModel):
    """토큰 응답 스키마"""
    
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    expires_in: int = Field(..., description="만료 시간 (초)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class LoginResponse(TokenResponse):
    """로그인 응답 스키마"""
    
    refresh_token: str = Field(..., description="리프레시 토큰")
    user: UserInfoResponse = Field(..., description="사용자 정보")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "user_id": "user-123",
                    "username": "admin",
                    "email": "admin@datagenie.com",
                    "role": "admin",
                    "permissions": [
                        "analysis:execute",
                        "query:read",
                        "user:manage"
                    ]
                }
            }
        }


class TokenData(BaseModel):
    """토큰 데이터 스키마 (내부 사용)"""
    
    user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)


class PasswordChangeRequest(BaseModel):
    """비밀번호 변경 요청 스키마"""
    
    current_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="현재 비밀번호"
    )
    
    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="새 비밀번호"
    )
    
    confirm_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="새 비밀번호 확인"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }


class UserRegistrationRequest(BaseModel):
    """사용자 등록 요청 스키마"""
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="사용자명"
    )
    
    email: EmailStr = Field(..., description="이메일")
    
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="비밀번호"
    )
    
    confirm_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="비밀번호 확인"
    )
    
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="전체 이름"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "confirm_password": "password123",
                "full_name": "홍길동"
            }
        }
