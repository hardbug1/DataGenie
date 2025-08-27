"""
API Dependencies

Clean Architecture: Dependency Injection
FastAPI 의존성 주입을 위한 팩토리 함수들
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import structlog

from app.use_cases.analysis.execute_analysis_use_case import ExecuteAnalysisUseCase
from app.infrastructure.di_container import get_di_container
from app.core.auth.jwt_manager import JWTManager, TokenType
from app.core.security.sql_validator import SQLSecurityValidator
from app.core.security.pii_masker import PIIMasker

logger = structlog.get_logger(__name__)
security = HTTPBearer()

# 보안 컴포넌트 싱글톤 인스턴스
_jwt_manager = None
_sql_validator = None
_pii_masker = None


def get_jwt_manager() -> JWTManager:
    """JWT 관리자 인스턴스 반환"""
    global _jwt_manager
    if _jwt_manager is None:
        _jwt_manager = JWTManager()
    return _jwt_manager


def get_sql_validator() -> SQLSecurityValidator:
    """SQL 보안 검증기 인스턴스 반환"""
    global _sql_validator
    if _sql_validator is None:
        _sql_validator = SQLSecurityValidator()
    return _sql_validator


def get_pii_masker() -> PIIMasker:
    """PII 마스킹 시스템 인스턴스 반환"""
    global _pii_masker
    if _pii_masker is None:
        _pii_masker = PIIMasker()
    return _pii_masker


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> Dict[str, Any]:
    """
    현재 사용자 정보 조회
    
    JWT 토큰 검증을 통한 사용자 인증
    """
    try:
        token = credentials.credentials
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증 토큰이 필요합니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # JWT 토큰 검증
        validation_result = jwt_manager.validate_token(token)
        
        if not validation_result.is_valid or not validation_result.payload:
            logger.warning(
                "토큰 검증 실패",
                extra={
                    "error": validation_result.error_message,
                    "token_hash": token[:16] + "..." if len(token) > 16 else token
                }
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=validation_result.error_message or "유효하지 않은 인증 토큰입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = validation_result.payload
        
        # 액세스 토큰인지 확인
        if payload.token_type != TokenType.ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="액세스 토큰이 필요합니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 사용자 정보 반환
        return {
            "user_id": payload.user_id,
            "username": payload.username,
            "email": payload.email,
            "role": payload.role,
            "permissions": payload.permissions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("사용자 인증 중 오류 발생", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 처리 중 오류가 발생했습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_execute_analysis_use_case() -> ExecuteAnalysisUseCase:
    """
    분석 실행 Use Case 의존성 주입
    
    Clean Architecture: Composition Root
    의존성 주입 컨테이너에서 Use Case를 가져옵니다.
    """
    try:
        container = get_di_container()
        return container.get_execute_analysis_use_case()
        
    except Exception as e:
        logger.error("Use Case 의존성 주입 오류", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서비스 초기화 오류가 발생했습니다"
        )


# 추가 의존성 함수들 (향후 구현)

async def get_query_history_use_case():
    """쿼리 이력 Use Case 의존성 주입"""
    # TODO: 구현 예정
    pass


async def get_user_management_use_case():
    """사용자 관리 Use Case 의존성 주입"""
    # TODO: 구현 예정
    pass


async def get_connection_management_use_case():
    """연결 관리 Use Case 의존성 주입"""
    # TODO: 구현 예정
    pass
