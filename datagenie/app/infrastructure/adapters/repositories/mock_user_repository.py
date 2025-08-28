"""
Mock User Repository

개발 및 테스트용 임시 사용자 저장소
실제 데이터베이스 구현 전까지 사용
"""

from typing import Optional, List
from datetime import datetime
import structlog

from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.models.user import User
from app.use_cases.auth.authenticate_user_use_case import AuthenticateUserUseCase

logger = structlog.get_logger(__name__)


class MockUserRepository(IUserRepository):
    """
    Mock 사용자 저장소
    
    Clean Architecture: 도메인 인터페이스의 임시 구현체
    실제 데이터베이스 연동 전까지 메모리에 데이터 저장
    """
    
    def __init__(self):
        """메모리 저장소 초기화"""
        self._users: dict[str, User] = {}
        
        # 기본 테스트 사용자들 생성
        self._create_default_users()
        
        logger.info("Mock User Repository 초기화")
    
    def _create_default_users(self):
        """기본 테스트 사용자들 생성"""
        # 관리자 사용자
        admin_user = User(
            id="admin-user-id",
            username="admin",
            email="admin@datagenie.com",
            full_name="관리자",
            hashed_password=AuthenticateUserUseCase.hash_password("admin123"),
            role="admin",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # 일반 사용자
        regular_user = User(
            id="user-user-id",
            username="user",
            email="user@datagenie.com",
            full_name="일반 사용자",
            hashed_password=AuthenticateUserUseCase.hash_password("user123"),
            role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # 분석가 사용자
        analyst_user = User(
            id="analyst-user-id",
            username="analyst",
            email="analyst@datagenie.com",
            full_name="데이터 분석가",
            hashed_password=AuthenticateUserUseCase.hash_password("analyst123"),
            role="analyst",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # 비활성 사용자
        inactive_user = User(
            id="inactive-user-id",
            username="inactive",
            email="inactive@datagenie.com",
            full_name="비활성 사용자",
            hashed_password=AuthenticateUserUseCase.hash_password("inactive123"),
            role="user",
            is_active=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._users[admin_user.id] = admin_user
        self._users[regular_user.id] = regular_user
        self._users[analyst_user.id] = analyst_user
        self._users[inactive_user.id] = inactive_user
        
        logger.info(
            "기본 테스트 사용자들 생성됨",
            user_count=len(self._users)
        )
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """
        ID로 사용자 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            찾은 사용자 또는 None
        """
        user = self._users.get(user_id)
        if user:
            logger.debug("사용자 조회됨", user_id=user_id)
        else:
            logger.debug("사용자 없음", user_id=user_id)
        return user
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """
        사용자명으로 사용자 조회
        
        Args:
            username: 사용자명
            
        Returns:
            찾은 사용자 또는 None
        """
        for user in self._users.values():
            if user.username == username:
                logger.debug("사용자명으로 조회됨", username=username)
                return user
        
        logger.debug("사용자명으로 조회 실패", username=username)
        return None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자 조회
        
        Args:
            email: 이메일 주소
            
        Returns:
            찾은 사용자 또는 None
        """
        for user in self._users.values():
            if user.email == email:
                logger.debug("이메일로 조회됨", email=email)
                return user
        
        logger.debug("이메일로 조회 실패", email=email)
        return None
    
    async def save(self, user: User) -> None:
        """
        사용자 저장
        
        Args:
            user: 저장할 사용자
        """
        self._users[user.id] = user
        logger.debug(
            "사용자 저장됨",
            user_id=user.id,
            username=user.username
        )
    
    async def delete_by_id(self, user_id: str) -> bool:
        """
        ID로 사용자 삭제
        
        Args:
            user_id: 삭제할 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        if user_id in self._users:
            del self._users[user_id]
            logger.debug("사용자 삭제됨", user_id=user_id)
            return True
        else:
            logger.debug("삭제할 사용자 없음", user_id=user_id)
            return False
    
    async def find_all(
        self, 
        limit: int = 100, 
        offset: int = 0,
        active_only: bool = True
    ) -> List[User]:
        """
        사용자 목록 조회
        
        Args:
            limit: 조회할 최대 개수
            offset: 시작 위치
            active_only: 활성 사용자만 조회할지 여부
            
        Returns:
            사용자 목록
        """
        users = list(self._users.values())
        
        if active_only:
            users = [user for user in users if user.is_active]
        
        # 생성 시간 역순 정렬
        users.sort(key=lambda u: u.created_at, reverse=True)
        
        # 페이지네이션 적용
        result = users[offset:offset + limit]
        
        logger.debug(
            "사용자 목록 조회됨",
            total_count=len(users),
            returned_count=len(result),
            limit=limit,
            offset=offset,
            active_only=active_only
        )
        
        return result
    
    async def count_users(self, active_only: bool = True) -> int:
        """
        사용자 수 조회
        
        Args:
            active_only: 활성 사용자만 카운트할지 여부
            
        Returns:
            사용자 수
        """
        users = list(self._users.values())
        
        if active_only:
            users = [user for user in users if user.is_active]
        
        count = len(users)
        logger.debug("사용자 수 조회됨", count=count, active_only=active_only)
        
        return count
    
    async def update_last_login(self, user_id: str) -> None:
        """
        마지막 로그인 시간 업데이트
        
        Args:
            user_id: 사용자 ID
        """
        user = self._users.get(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            logger.debug("마지막 로그인 시간 업데이트됨", user_id=user_id)
        else:
            logger.warning("로그인 시간 업데이트할 사용자 없음", user_id=user_id)
    
    # 개발/디버깅용 메서드들
    
    def get_all_users(self) -> List[User]:
        """모든 사용자 반환 (개발용)"""
        return list(self._users.values())
    
    def clear_all(self) -> None:
        """모든 사용자 삭제 (테스트용)"""
        self._users.clear()
        logger.debug("모든 사용자 삭제됨")
    
    def get_user_count(self) -> int:
        """저장된 사용자 수 반환"""
        return len(self._users)
    
    def get_default_credentials(self) -> dict:
        """기본 사용자 인증 정보 반환 (개발용)"""
        return {
            "admin": {"username": "admin", "password": "admin123", "role": "admin"},
            "user": {"username": "user", "password": "user123", "role": "user"},
            "analyst": {"username": "analyst", "password": "analyst123", "role": "analyst"},
            "inactive": {"username": "inactive", "password": "inactive123", "role": "user", "active": False}
        }
