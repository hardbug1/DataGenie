"""
SQLAlchemy Query Repository

실제 데이터베이스를 사용하는 쿼리 저장소 구현
Clean Architecture: Infrastructure Layer
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import desc, and_
import structlog

from app.domain.entities.analysis_query import AnalysisQuery, QueryType, QueryStatus
from app.domain.interfaces.repositories.query_repository import IQueryRepository
from app.models.query_history import QueryHistory
from app.config.database import get_async_session

logger = structlog.get_logger(__name__)


class SQLAlchemyQueryRepository(IQueryRepository):
    """
    SQLAlchemy 기반 쿼리 저장소
    
    Clean Architecture: Infrastructure Layer
    도메인 엔티티를 데이터베이스 모델로 변환하여 저장
    """
    
    def __init__(self, session_factory=None):
        """
        저장소 초기화
        
        Args:
            session_factory: 데이터베이스 세션 팩토리 (테스트용)
        """
        self._session_factory = session_factory or get_async_session
        logger.info("SQLAlchemy Query Repository 초기화")
    
    async def save(self, query: AnalysisQuery) -> None:
        """
        쿼리 저장
        
        Args:
            query: 저장할 분석 쿼리 도메인 엔티티
        """
        async with self._session_factory() as session:
            try:
                # 기존 쿼리 확인
                existing_query = await session.get(QueryHistory, query.id)
                
                if existing_query:
                    # 업데이트
                    existing_query.question = query.question
                    existing_query.query_type = query.query_type.value
                    existing_query.status = query.status.value
                    existing_query.connection_id = query.connection_id
                    existing_query.execution_time_ms = query.execution_time_ms
                    existing_query.error_message = query.error_message
                    existing_query.updated_at = query.updated_at
                    
                    logger.debug("쿼리 업데이트됨", query_id=query.id)
                else:
                    # 새로 생성
                    db_query = QueryHistory(
                        id=query.id,
                        user_id=query.user_id,
                        question=query.question,
                        query_type=query.query_type.value,
                        status=query.status.value,
                        connection_id=query.connection_id,
                        execution_time_ms=query.execution_time_ms,
                        error_message=query.error_message,
                        created_at=query.created_at,
                        updated_at=query.updated_at
                    )
                    session.add(db_query)
                    
                    logger.debug("새 쿼리 생성됨", query_id=query.id)
                
                await session.commit()
                
                logger.info(
                    "쿼리 저장 완료",
                    query_id=query.id,
                    user_id=query.user_id,
                    status=query.status.value
                )
                
            except Exception as e:
                await session.rollback()
                logger.error(
                    "쿼리 저장 실패",
                    query_id=query.id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def find_by_id(self, query_id: str) -> Optional[AnalysisQuery]:
        """
        ID로 쿼리 조회
        
        Args:
            query_id: 쿼리 ID
            
        Returns:
            찾은 쿼리 도메인 엔티티 또는 None
        """
        async with self._session_factory() as session:
            try:
                db_query = await session.get(QueryHistory, query_id)
                
                if db_query:
                    domain_query = self._to_domain_entity(db_query)
                    logger.debug("쿼리 조회됨", query_id=query_id)
                    return domain_query
                else:
                    logger.debug("쿼리 없음", query_id=query_id)
                    return None
                    
            except Exception as e:
                logger.error(
                    "쿼리 조회 실패",
                    query_id=query_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
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
            쿼리 도메인 엔티티 목록
        """
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(QueryHistory)
                    .where(QueryHistory.user_id == user_id)
                    .order_by(desc(QueryHistory.created_at))
                    .limit(limit)
                    .offset(offset)
                )
                
                result = await session.execute(stmt)
                db_queries = result.scalars().all()
                
                domain_queries = [
                    self._to_domain_entity(db_query) 
                    for db_query in db_queries
                ]
                
                logger.debug(
                    "사용자 쿼리 조회됨",
                    user_id=user_id,
                    returned_count=len(domain_queries),
                    limit=limit,
                    offset=offset
                )
                
                return domain_queries
                
            except Exception as e:
                logger.error(
                    "사용자 쿼리 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def delete_by_id(self, query_id: str) -> bool:
        """
        ID로 쿼리 삭제
        
        Args:
            query_id: 삭제할 쿼리 ID
            
        Returns:
            삭제 성공 여부
        """
        async with self._session_factory() as session:
            try:
                db_query = await session.get(QueryHistory, query_id)
                
                if db_query:
                    await session.delete(db_query)
                    await session.commit()
                    
                    logger.info("쿼리 삭제됨", query_id=query_id)
                    return True
                else:
                    logger.debug("삭제할 쿼리 없음", query_id=query_id)
                    return False
                    
            except Exception as e:
                await session.rollback()
                logger.error(
                    "쿼리 삭제 실패",
                    query_id=query_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def find_by_status(
        self, 
        status: QueryStatus, 
        limit: int = 100
    ) -> List[AnalysisQuery]:
        """
        상태별 쿼리 조회
        
        Args:
            status: 쿼리 상태
            limit: 조회할 최대 개수
            
        Returns:
            해당 상태의 쿼리 목록
        """
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(QueryHistory)
                    .where(QueryHistory.status == status.value)
                    .order_by(desc(QueryHistory.created_at))
                    .limit(limit)
                )
                
                result = await session.execute(stmt)
                db_queries = result.scalars().all()
                
                domain_queries = [
                    self._to_domain_entity(db_query) 
                    for db_query in db_queries
                ]
                
                logger.debug(
                    "상태별 쿼리 조회됨",
                    status=status.value,
                    count=len(domain_queries)
                )
                
                return domain_queries
                
            except Exception as e:
                logger.error(
                    "상태별 쿼리 조회 실패",
                    status=status.value,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def count_by_user_id(self, user_id: str) -> int:
        """
        사용자별 쿼리 수 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            쿼리 수
        """
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(QueryHistory)
                    .where(QueryHistory.user_id == user_id)
                )
                
                result = await session.execute(stmt)
                count = len(result.scalars().all())
                
                logger.debug("사용자 쿼리 수 조회됨", user_id=user_id, count=count)
                return count
                
            except Exception as e:
                logger.error(
                    "사용자 쿼리 수 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    def _to_domain_entity(self, db_query: QueryHistory) -> AnalysisQuery:
        """
        데이터베이스 모델을 도메인 엔티티로 변환
        
        Args:
            db_query: 데이터베이스 쿼리 모델
            
        Returns:
            도메인 쿼리 엔티티
        """
        return AnalysisQuery(
            id=db_query.id,
            user_id=db_query.user_id,
            question=db_query.question,
            query_type=QueryType(db_query.query_type),
            status=QueryStatus(db_query.status),
            connection_id=db_query.connection_id,
            execution_time_ms=db_query.execution_time_ms,
            error_message=db_query.error_message,
            created_at=db_query.created_at,
            updated_at=db_query.updated_at
        )
