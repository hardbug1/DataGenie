"""
Authenticate User Use Case

사용자 인증을 처리하는 Use Case
Clean Architecture: Application Business Rules
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import structlog
from passlib.context import CryptContext

from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.models.user import User

logger = structlog.get_logger(__name__)

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class AuthenticationRequest:
    """인증 요청 DTO"""
    username: str
    password: str


@dataclass
class AuthenticationResult:
    """인증 결과 DTO"""
    success: bool
    user_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class AuthenticateUserUseCase:
    """
    사용자 인증 Use Case
    
    Clean Architecture: Application Business Rules
    사용자 인증 비즈니스 로직을 담당
    """
    
    def __init__(self, user_repository: IUserRepository):
        """
        의존성 주입을 통한 초기화
        
        Args:
            user_repository: 사용자 저장소 인터페이스
        """
        self._user_repository = user_repository
    
    async def execute(self, request: AuthenticationRequest) -> AuthenticationResult:
        """
        사용자 인증 실행
        
        Args:
            request: 인증 요청
            
        Returns:
            AuthenticationResult: 인증 결과
        """
        try:
            logger.info(
                "사용자 인증 시작",
                username=request.username
            )
            
            # 1. 입력 검증
            if not self._validate_input(request):
                return AuthenticationResult(
                    success=False,
                    error_message="사용자명과 비밀번호를 입력해주세요"
                )
            
            # 2. 사용자 조회
            user = await self._user_repository.find_by_username(request.username)
            
            if not user:
                logger.warning("존재하지 않는 사용자", username=request.username)
                return AuthenticationResult(
                    success=False,
                    error_message="잘못된 사용자명 또는 비밀번호입니다"
                )
            
            # 3. 사용자 상태 확인
            if not user.is_active:
                logger.warning("비활성 사용자 로그인 시도", username=request.username)
                return AuthenticationResult(
                    success=False,
                    error_message="계정이 비활성화되었습니다"
                )
            
            # 4. 비밀번호 검증
            if not self._verify_password(request.password, user.hashed_password):
                logger.warning("잘못된 비밀번호", username=request.username)
                return AuthenticationResult(
                    success=False,
                    error_message="잘못된 사용자명 또는 비밀번호입니다"
                )
            
            # 5. 사용자 데이터 구성
            user_data = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "permissions": self._get_user_permissions(user.role),
                "full_name": user.full_name,
                "is_active": user.is_active
            }
            
            logger.info(
                "사용자 인증 성공",
                user_id=user.id,
                username=user.username,
                role=user.role
            )
            
            return AuthenticationResult(
                success=True,
                user_data=user_data
            )
            
        except Exception as e:
            logger.error(
                "사용자 인증 중 오류 발생",
                username=request.username,
                error=str(e),
                exc_info=True
            )
            return AuthenticationResult(
                success=False,
                error_message="인증 처리 중 오류가 발생했습니다"
            )
    
    def _validate_input(self, request: AuthenticationRequest) -> bool:
        """입력 검증"""
        if not request.username or not request.username.strip():
            return False
        if not request.password or len(request.password) < 1:
            return False
        return True
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error("비밀번호 검증 오류", error=str(e))
            return False
    
    def _get_user_permissions(self, role: str) -> list[str]:
        """역할별 권한 반환"""
        role_permissions = {
            "admin": [
                "analysis:execute",
                "query:read",
                "query:write",
                "query:delete",
                "user:manage",
                "connection:manage",
                "connection:create",
                "connection:delete",
                "file:upload",
                "file:download",
                "system:monitor"
            ],
            "analyst": [
                "analysis:execute",
                "query:read",
                "query:write",
                "connection:create",
                "file:upload",
                "file:download"
            ],
            "user": [
                "analysis:execute",
                "query:read",
                "file:upload"
            ]
        }
        
        return role_permissions.get(role, ["analysis:execute", "query:read"])
    
    @staticmethod
    def hash_password(password: str) -> str:
        """비밀번호 해싱 (사용자 생성시 사용)"""
        return pwd_context.hash(password)


class AuthenticationError(Exception):
    """인증 관련 예외"""
    pass
