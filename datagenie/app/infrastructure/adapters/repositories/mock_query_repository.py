"""
Mock Query Repository

개발 및 테스트용 임시 구현체
실제 데이터베이스 구현 전까지 사용
"""

from typing import List, Optional
import structlog

from app.domain.entities.analysis_query import AnalysisQuery
from app.domain.interfaces.repositories.query_repository import IQueryRepository

logger = structlog.get_logger(__name__)


class MockQueryRepository(IQueryRepository):
    """
    Mock 쿼리 저장소
    
    Clean Architecture: 도메인 인터페이스의 임시 구현체
    실제 데이터베이스 연동 전까지 메모리에 데이터 저장
    """
    
    def __init__(self):
        """메모리 저장소 초기화"""
        self._queries: dict[str, AnalysisQuery] = {}
        logger.info("Mock Query Repository 초기화")
    
    async def save(self, query: AnalysisQuery) -> None:
        """
        쿼리 저장
        
        Args:
            query: 저장할 분석 쿼리
        """
        self._queries[query.id] = query
        logger.debug(
            "쿼리 저장됨",
            query_id=query.id,
            user_id=query.user_id,
            status=query.status.value
        )
    
    async def find_by_id(self, query_id: str) -> Optional[AnalysisQuery]:
        """
        ID로 쿼리 조회
        
        Args:
            query_id: 쿼리 ID
            
        Returns:
            찾은 쿼리 또는 None
        """
        query = self._queries.get(query_id)
        if query:
            logger.debug("쿼리 조회됨", query_id=query_id)
        else:
            logger.debug("쿼리 없음", query_id=query_id)
        return query
    
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
        user_queries = [
            query for query in self._queries.values()
            if query.user_id == user_id
        ]
        
        # 생성 시간 역순 정렬
        user_queries.sort(key=lambda q: q.created_at, reverse=True)
        
        # 페이지네이션 적용
        result = user_queries[offset:offset + limit]
        
        logger.debug(
            "사용자 쿼리 조회됨",
            user_id=user_id,
            total_count=len(user_queries),
            returned_count=len(result),
            limit=limit,
            offset=offset
        )
        
        return result
    
    async def delete_by_id(self, query_id: str) -> bool:
        """
        ID로 쿼리 삭제
        
        Args:
            query_id: 삭제할 쿼리 ID
            
        Returns:
            삭제 성공 여부
        """
        if query_id in self._queries:
            del self._queries[query_id]
            logger.debug("쿼리 삭제됨", query_id=query_id)
            return True
        else:
            logger.debug("삭제할 쿼리 없음", query_id=query_id)
            return False
    
    # 개발/디버깅용 메서드들
    
    def get_all_queries(self) -> List[AnalysisQuery]:
        """모든 쿼리 반환 (개발용)"""
        return list(self._queries.values())
    
    def clear_all(self) -> None:
        """모든 쿼리 삭제 (테스트용)"""
        self._queries.clear()
        logger.debug("모든 쿼리 삭제됨")
    
    def get_query_count(self) -> int:
        """저장된 쿼리 수 반환"""
        return len(self._queries)
