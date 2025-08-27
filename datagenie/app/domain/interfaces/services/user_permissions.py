"""
User Permissions Interface

Clean Architecture: 도메인에서 정의하는 사용자 권한 서비스 인터페이스
"""

from abc import ABC, abstractmethod


class IUserPermissions(ABC):
    """
    사용자 권한 서비스 인터페이스
    
    Clean Architecture: 도메인에서 정의하는 권한 관리 계약
    """
    
    @abstractmethod
    async def can_execute_analysis(self, user_id: str) -> bool:
        """
        사용자가 분석을 실행할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            분석 실행 권한 여부
        """
        pass
    
    @abstractmethod
    async def can_access_connection(self, user_id: str, connection_id: str) -> bool:
        """
        사용자가 특정 데이터베이스 연결에 접근할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            connection_id: 데이터베이스 연결 ID
            
        Returns:
            연결 접근 권한 여부
        """
        pass
    
    @abstractmethod
    async def get_user_role(self, user_id: str) -> str:
        """
        사용자 역할 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            사용자 역할
        """
        pass
