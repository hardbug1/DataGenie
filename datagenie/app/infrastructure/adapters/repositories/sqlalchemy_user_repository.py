"""
SQLAlchemy User Repository

실제 데이터베이스를 사용하는 사용자 저장소 구현
Clean Architecture: Infrastructure Layer
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, and_, func
from datetime import datetime
import structlog

from app.domain.interfaces.repositories.user_repository import IUserRepository
from app.models.user import User
from app.config.database import get_async_session

logger = structlog.get_logger(__name__)


class SQLAlchemyUserRepository(IUserRepository):
    """
    SQLAlchemy 기반 사용자 저장소
    
    Clean Architecture: Infrastructure Layer
    사용자 데이터를 데이터베이스에서 관리
    """
    
    def __init__(self, session_factory=None):
        """
        저장소 초기화
        
        Args:
            session_factory: 데이터베이스 세션 팩토리 (테스트용)
        """
        self._session_factory = session_factory or get_async_session
        logger.info("SQLAlchemy User Repository 초기화")
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """
        ID로 사용자 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            찾은 사용자 또는 None
        """
        async with self._session_factory() as session:
            try:
                user = await session.get(User, user_id)
                
                if user:
                    logger.debug("사용자 조회됨", user_id=user_id)
                else:
                    logger.debug("사용자 없음", user_id=user_id)
                
                return user
                
            except Exception as e:
                logger.error(
                    "사용자 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """
        사용자명으로 사용자 조회
        
        Args:
            username: 사용자명
            
        Returns:
            찾은 사용자 또는 None
        """
        async with self._session_factory() as session:
            try:
                stmt = select(User).where(User.username == username)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    logger.debug("사용자명으로 조회됨", username=username)
                else:
                    logger.debug("사용자명으로 조회 실패", username=username)
                
                return user
                
            except Exception as e:
                logger.error(
                    "사용자명 조회 실패",
                    username=username,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        이메일로 사용자 조회
        
        Args:
            email: 이메일 주소
            
        Returns:
            찾은 사용자 또는 None
        """
        async with self._session_factory() as session:
            try:
                stmt = select(User).where(User.email == email)
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    logger.debug("이메일로 조회됨", email=email)
                else:
                    logger.debug("이메일로 조회 실패", email=email)
                
                return user
                
            except Exception as e:
                logger.error(
                    "이메일 조회 실패",
                    email=email,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def save(self, user: User) -> None:
        """
        사용자 저장
        
        Args:
            user: 저장할 사용자
        """
        async with self._session_factory() as session:
            try:
                # 기존 사용자 확인
                existing_user = await session.get(User, user.id)
                
                if existing_user:
                    # 업데이트
                    existing_user.username = user.username
                    existing_user.email = user.email
                    existing_user.full_name = user.full_name
                    existing_user.hashed_password = user.hashed_password
                    existing_user.role = user.role
                    existing_user.is_active = user.is_active
                    existing_user.last_login_at = user.last_login_at
                    existing_user.updated_at = datetime.utcnow()
                    
                    logger.debug("사용자 업데이트됨", user_id=user.id)
                else:
                    # 새로 생성
                    session.add(user)
                    logger.debug("새 사용자 생성됨", user_id=user.id)
                
                await session.commit()
                
                logger.info(
                    "사용자 저장 완료",
                    user_id=user.id,
                    username=user.username
                )
                
            except Exception as e:
                await session.rollback()
                logger.error(
                    "사용자 저장 실패",
                    user_id=user.id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def delete_by_id(self, user_id: str) -> bool:
        """
        ID로 사용자 삭제
        
        Args:
            user_id: 삭제할 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        async with self._session_factory() as session:
            try:
                user = await session.get(User, user_id)
                
                if user:
                    await session.delete(user)
                    await session.commit()
                    
                    logger.info("사용자 삭제됨", user_id=user_id)
                    return True
                else:
                    logger.debug("삭제할 사용자 없음", user_id=user_id)
                    return False
                    
            except Exception as e:
                await session.rollback()
                logger.error(
                    "사용자 삭제 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                raise
    
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
        async with self._session_factory() as session:
            try:
                stmt = select(User)
                
                if active_only:
                    stmt = stmt.where(User.is_active == True)
                
                stmt = (
                    stmt.order_by(desc(User.created_at))
                    .limit(limit)
                    .offset(offset)
                )
                
                result = await session.execute(stmt)
                users = result.scalars().all()
                
                logger.debug(
                    "사용자 목록 조회됨",
                    count=len(users),
                    limit=limit,
                    offset=offset,
                    active_only=active_only
                )
                
                return list(users)
                
            except Exception as e:
                logger.error(
                    "사용자 목록 조회 실패",
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def count_users(self, active_only: bool = True) -> int:
        """
        사용자 수 조회
        
        Args:
            active_only: 활성 사용자만 카운트할지 여부
            
        Returns:
            사용자 수
        """
        async with self._session_factory() as session:
            try:
                stmt = select(func.count(User.id))
                
                if active_only:
                    stmt = stmt.where(User.is_active == True)
                
                result = await session.execute(stmt)
                count = result.scalar()
                
                logger.debug(
                    "사용자 수 조회됨",
                    count=count,
                    active_only=active_only
                )
                
                return count or 0
                
            except Exception as e:
                logger.error(
                    "사용자 수 조회 실패",
                    error=str(e),
                    exc_info=True
                )
                raise
    
    async def update_last_login(self, user_id: str) -> None:
        """
        마지막 로그인 시간 업데이트
        
        Args:
            user_id: 사용자 ID
        """
        async with self._session_factory() as session:
            try:
                user = await session.get(User, user_id)
                
                if user:
                    user.last_login_at = datetime.utcnow()
                    await session.commit()
                    
                    logger.debug("마지막 로그인 시간 업데이트됨", user_id=user_id)
                else:
                    logger.warning("로그인 시간 업데이트할 사용자 없음", user_id=user_id)
                
            except Exception as e:
                await session.rollback()
                logger.error(
                    "마지막 로그인 시간 업데이트 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                raise
