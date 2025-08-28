"""
User Repository Interface

사용자 저장소 도메인 인터페이스
Clean Architecture: Domain Layer
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.user import User


class IUserRepository(ABC):
    """
    사용자 저장소 인터페이스
    
    Clean Architecture: Domain Layer Interface
    사용자 데이터 접근을 위한 추상 인터페이스
    """
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """
        ID로 사용자 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            찾은 사용자 또는 None
        """
        pass
    
    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """
        사용자명으로 사용자 조회
        
        Args:
            username: 사용자명
            
        Returns:
            찾은 사용자 또는 None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자 조회
        
        Args:
            email: 이메일 주소
            
        Returns:
            찾은 사용자 또는 None
        """
        pass
    
    @abstractmethod
    async def save(self, user: User) -> None:
        """
        사용자 저장
        
        Args:
            user: 저장할 사용자
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, user_id: str) -> bool:
        """
        ID로 사용자 삭제
        
        Args:
            user_id: 삭제할 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    async def count_users(self, active_only: bool = True) -> int:
        """
        사용자 수 조회
        
        Args:
            active_only: 활성 사용자만 카운트할지 여부
            
        Returns:
            사용자 수
        """
        pass
    
    @abstractmethod
    async def update_last_login(self, user_id: str) -> None:
        """
        마지막 로그인 시간 업데이트
        
        Args:
            user_id: 사용자 ID
        """
        pass
