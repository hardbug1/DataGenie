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

logger = structlog.get_logger(__name__)
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    현재 사용자 정보 조회
    
    TODO: JWT 토큰 검증 로직 구현 필요
    현재는 임시 구현으로 더미 사용자 반환
    """
    try:
        # TODO: JWT 토큰 검증 구현
        # 현재는 개발용 더미 사용자 반환
        token = credentials.credentials
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증 토큰이 필요합니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 임시 더미 사용자 (실제로는 JWT에서 추출)
        return {
            "user_id": "dummy-user-id",
            "username": "test_user",
            "role": "user",
            "permissions": ["analysis:execute", "query:read"]
        }
        
    except Exception as e:
        logger.error("사용자 인증 오류", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다",
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
