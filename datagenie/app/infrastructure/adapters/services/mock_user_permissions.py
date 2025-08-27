"""
Mock User Permissions Service

개발 및 테스트용 임시 권한 서비스
실제 인증/인가 시스템 구현 전까지 사용
"""

import structlog

from app.domain.interfaces.services.user_permissions import IUserPermissions

logger = structlog.get_logger(__name__)


class MockUserPermissions(IUserPermissions):
    """
    Mock 사용자 권한 서비스
    
    Clean Architecture: 도메인 인터페이스의 임시 구현체
    실제 인증/인가 시스템 구현 전까지 모든 권한을 허용
    """
    
    def __init__(self):
        """Mock 권한 서비스 초기화"""
        # 테스트용 사용자 데이터
        self._users = {
            "dummy-user-id": {
                "username": "test_user",
                "role": "user",
                "permissions": ["analysis:execute", "query:read", "file:upload"],
                "is_active": True
            },
            "admin-user-id": {
                "username": "admin_user",
                "role": "admin",
                "permissions": ["*"],  # 모든 권한
                "is_active": True
            }
        }
        
        # 테스트용 연결 권한
        self._connection_permissions = {
            "dummy-user-id": ["conn-1", "conn-2"],
            "admin-user-id": ["*"]  # 모든 연결
        }
        
        logger.info("Mock User Permissions 초기화")
    
    async def can_execute_analysis(self, user_id: str) -> bool:
        """
        사용자가 분석을 실행할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            분석 실행 권한 여부
        """
        user = self._users.get(user_id)
        
        if not user:
            logger.warning("존재하지 않는 사용자", user_id=user_id)
            return False
        
        if not user.get("is_active", False):
            logger.warning("비활성 사용자", user_id=user_id)
            return False
        
        permissions = user.get("permissions", [])
        has_permission = (
            "*" in permissions or 
            "analysis:execute" in permissions
        )
        
        logger.debug(
            "분석 실행 권한 확인",
            user_id=user_id,
            has_permission=has_permission,
            user_role=user.get("role")
        )
        
        return has_permission
    
    async def can_access_connection(self, user_id: str, connection_id: str) -> bool:
        """
        사용자가 특정 데이터베이스 연결에 접근할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            connection_id: 데이터베이스 연결 ID
            
        Returns:
            연결 접근 권한 여부
        """
        user = self._users.get(user_id)
        
        if not user or not user.get("is_active", False):
            logger.warning("유효하지 않은 사용자", user_id=user_id)
            return False
        
        allowed_connections = self._connection_permissions.get(user_id, [])
        has_access = (
            "*" in allowed_connections or 
            connection_id in allowed_connections
        )
        
        logger.debug(
            "연결 접근 권한 확인",
            user_id=user_id,
            connection_id=connection_id,
            has_access=has_access,
            allowed_connections=allowed_connections
        )
        
        return has_access
    
    async def get_user_role(self, user_id: str) -> str:
        """
        사용자 역할 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            사용자 역할
        """
        user = self._users.get(user_id)
        
        if not user:
            logger.warning("존재하지 않는 사용자", user_id=user_id)
            return "unknown"
        
        role = user.get("role", "user")
        logger.debug("사용자 역할 조회", user_id=user_id, role=role)
        
        return role
    
    # 개발/테스트용 메서드들
    
    def add_user(self, user_id: str, user_data: dict) -> None:
        """사용자 추가 (테스트용)"""
        self._users[user_id] = user_data
        logger.debug("사용자 추가됨", user_id=user_id)
    
    def add_connection_permission(self, user_id: str, connection_id: str) -> None:
        """연결 권한 추가 (테스트용)"""
        if user_id not in self._connection_permissions:
            self._connection_permissions[user_id] = []
        
        if connection_id not in self._connection_permissions[user_id]:
            self._connection_permissions[user_id].append(connection_id)
            logger.debug("연결 권한 추가됨", user_id=user_id, connection_id=connection_id)
    
    def get_all_users(self) -> dict:
        """모든 사용자 반환 (개발용)"""
        return self._users.copy()
    
    def clear_all_users(self) -> None:
        """모든 사용자 삭제 (테스트용)"""
        self._users.clear()
        self._connection_permissions.clear()
        logger.debug("모든 사용자 데이터 삭제됨")
