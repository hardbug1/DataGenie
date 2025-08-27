"""
Authentication API Endpoints

Clean Architecture: Interface Adapters - Web Controllers
인증 관련 REST API 엔드포인트를 제공합니다.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import structlog

from app.core.auth.jwt_manager import JWTManager, AuthenticationError
from app.api.dependencies import get_jwt_manager, get_current_user
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserInfoResponse
)

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="사용자 로그인",
    description="사용자 인증 후 JWT 토큰을 발급합니다."
)
async def login(
    request: LoginRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> LoginResponse:
    """
    사용자 로그인
    
    TODO: 실제 사용자 인증 로직 구현 필요
    현재는 개발용 더미 구현
    """
    try:
        # TODO: 실제 사용자 인증 (데이터베이스 조회, 비밀번호 검증)
        # 현재는 개발용 더미 인증
        if request.username == "admin" and request.password == "admin123":
            user_data = {
                "user_id": "admin-user-id",
                "username": "admin",
                "email": "admin@datagenie.com",
                "role": "admin",
                "permissions": [
                    "analysis:execute",
                    "query:read",
                    "query:write",
                    "user:manage",
                    "connection:manage"
                ]
            }
        elif request.username == "user" and request.password == "user123":
            user_data = {
                "user_id": "test-user-id",
                "username": "user",
                "email": "user@datagenie.com",
                "role": "user",
                "permissions": [
                    "analysis:execute",
                    "query:read"
                ]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="잘못된 사용자명 또는 비밀번호입니다"
            )
        
        # JWT 토큰 생성
        access_token = jwt_manager.create_access_token(
            user_id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            permissions=user_data["permissions"]
        )
        
        refresh_token = jwt_manager.create_refresh_token(
            user_id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"]
        )
        
        logger.info(
            "사용자 로그인 성공",
            extra={
                "user_id": user_data["user_id"],
                "username": user_data["username"],
                "role": user_data["role"]
            }
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=jwt_manager.access_token_expire_minutes * 60,
            user=UserInfoResponse(
                user_id=user_data["user_id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                permissions=user_data["permissions"]
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("로그인 처리 중 오류 발생", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 처리 중 오류가 발생했습니다"
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="토큰 갱신",
    description="리프레시 토큰으로 새로운 액세스 토큰을 발급합니다."
)
async def refresh_token(
    request: RefreshTokenRequest,
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> TokenResponse:
    """리프레시 토큰으로 새 액세스 토큰 발급"""
    try:
        new_access_token = jwt_manager.refresh_access_token(request.refresh_token)
        
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 리프레시 토큰입니다"
            )
        
        logger.info("토큰 갱신 성공")
        
        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=jwt_manager.access_token_expire_minutes * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("토큰 갱신 중 오류 발생", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="토큰 갱신 중 오류가 발생했습니다"
        )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="로그아웃",
    description="현재 토큰을 무효화합니다."
)
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_user),
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> Dict[str, str]:
    """사용자 로그아웃 (토큰 블랙리스트 추가)"""
    try:
        # TODO: 실제로는 요청 헤더에서 토큰을 추출해야 함
        # 현재는 간단한 구현
        
        logger.info(
            "사용자 로그아웃",
            extra={
                "user_id": current_user["user_id"],
                "username": current_user["username"]
            }
        )
        
        return {"message": "로그아웃되었습니다"}
        
    except Exception as e:
        logger.error("로그아웃 처리 중 오류 발생", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그아웃 처리 중 오류가 발생했습니다"
        )


@router.get(
    "/me",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="현재 사용자 정보",
    description="현재 인증된 사용자의 정보를 반환합니다."
)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> UserInfoResponse:
    """현재 사용자 정보 조회"""
    return UserInfoResponse(
        user_id=current_user["user_id"],
        username=current_user["username"],
        email=current_user["email"],
        role=current_user["role"],
        permissions=current_user["permissions"]
    )


@router.get(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="토큰 검증",
    description="현재 토큰의 유효성을 검증합니다."
)
async def verify_token(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """토큰 유효성 검증"""
    return {
        "valid": True,
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }
