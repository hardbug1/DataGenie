"""
Query Repository Interface

Clean Architecture: 도메인에서 정의하는 쿼리 저장소 인터페이스
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.analysis_query import AnalysisQuery


class IQueryRepository(ABC):
    """
    쿼리 저장소 인터페이스
    
    Clean Architecture: 도메인 계층에서 정의하는 인터페이스로,
    인프라스트럭처 계층에서 구현됩니다.
    """
    
    @abstractmethod
    async def save(self, query: AnalysisQuery) -> None:
        """
        쿼리 저장
        
        Args:
            query: 저장할 분석 쿼리
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, query_id: str) -> Optional[AnalysisQuery]:
        """
        ID로 쿼리 조회
        
        Args:
            query_id: 쿼리 ID
            
        Returns:
            찾은 쿼리 또는 None
        """
        pass
    
    @abstractmethod
    async def find_by_user_id(
        self, 
        user_id: str, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[AnalysisQuery]:
        """
        사용자 ID로 쿼리 목록 조회
        
        Args:
            user_id: 사용자 ID
            limit: 조회할 최대 개수
            offset: 시작 위치
            
        Returns:
            쿼리 목록
        """
        pass
    
    @abstractmethod
    async def delete_by_id(self, query_id: str) -> bool:
        """
        ID로 쿼리 삭제
        
        Args:
            query_id: 삭제할 쿼리 ID
            
        Returns:
            삭제 성공 여부
        """
        pass
