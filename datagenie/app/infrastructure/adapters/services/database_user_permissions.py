"""
Database User Permissions Service

실제 데이터베이스를 사용하는 사용자 권한 서비스 구현
Clean Architecture: Infrastructure Layer
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
import structlog

from app.domain.interfaces.services.user_permissions import IUserPermissions
from app.models.user import User
from app.models.database_connection import DatabaseConnection
from app.config.database import get_async_session

logger = structlog.get_logger(__name__)


class DatabaseUserPermissions(IUserPermissions):
    """
    데이터베이스 기반 사용자 권한 서비스
    
    Clean Architecture: Infrastructure Layer
    실제 사용자 및 권한 데이터를 데이터베이스에서 조회
    """
    
    def __init__(self, session_factory=None):
        """
        권한 서비스 초기화
        
        Args:
            session_factory: 데이터베이스 세션 팩토리 (테스트용)
        """
        self._session_factory = session_factory or get_async_session
        logger.info("Database User Permissions 초기화")
    
    async def can_execute_analysis(self, user_id: str) -> bool:
        """
        사용자가 분석을 실행할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            분석 실행 권한 여부
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user:
                    logger.warning("존재하지 않는 사용자", user_id=user_id)
                    return False
                
                if not user.is_active:
                    logger.warning("비활성 사용자", user_id=user_id)
                    return False
                
                # 역할 기반 권한 확인
                has_permission = self._check_analysis_permission(user)
                
                logger.debug(
                    "분석 실행 권한 확인",
                    user_id=user_id,
                    has_permission=has_permission,
                    user_role=user.role,
                    is_active=user.is_active
                )
                
                return has_permission
                
            except Exception as e:
                logger.error(
                    "분석 실행 권한 확인 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                return False
    
    async def can_access_connection(self, user_id: str, connection_id: str) -> bool:
        """
        사용자가 특정 데이터베이스 연결에 접근할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            connection_id: 데이터베이스 연결 ID
            
        Returns:
            연결 접근 권한 여부
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user or not user.is_active:
                    logger.warning("유효하지 않은 사용자", user_id=user_id)
                    return False
                
                # 관리자는 모든 연결에 접근 가능
                if user.role == "admin":
                    logger.debug("관리자 권한으로 연결 접근 허용", user_id=user_id)
                    return True
                
                # 연결 소유자 확인
                connection = await self._get_connection_by_id(session, connection_id)
                
                if not connection:
                    logger.warning("존재하지 않는 연결", connection_id=connection_id)
                    return False
                
                # 연결 소유자이거나 공유된 연결인지 확인
                has_access = (
                    connection.user_id == user_id or
                    connection.is_shared or
                    self._check_connection_permission(user, connection)
                )
                
                logger.debug(
                    "연결 접근 권한 확인",
                    user_id=user_id,
                    connection_id=connection_id,
                    has_access=has_access,
                    is_owner=connection.user_id == user_id,
                    is_shared=connection.is_shared
                )
                
                return has_access
                
            except Exception as e:
                logger.error(
                    "연결 접근 권한 확인 실패",
                    user_id=user_id,
                    connection_id=connection_id,
                    error=str(e),
                    exc_info=True
                )
                return False
    
    async def get_user_role(self, user_id: str) -> str:
        """
        사용자 역할 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            사용자 역할
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user:
                    logger.warning("존재하지 않는 사용자", user_id=user_id)
                    return "unknown"
                
                role = user.role or "user"
                logger.debug("사용자 역할 조회", user_id=user_id, role=role)
                
                return role
                
            except Exception as e:
                logger.error(
                    "사용자 역할 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                return "unknown"
    
    async def get_accessible_connections(self, user_id: str) -> List[str]:
        """
        사용자가 접근 가능한 연결 목록 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            접근 가능한 연결 ID 목록
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user or not user.is_active:
                    logger.warning("유효하지 않은 사용자", user_id=user_id)
                    return []
                
                # 관리자는 모든 활성 연결에 접근 가능
                if user.role == "admin":
                    stmt = select(DatabaseConnection).where(
                        DatabaseConnection.is_active == True
                    )
                else:
                    # 일반 사용자는 본인 소유 또는 공유된 연결만 접근 가능
                    stmt = select(DatabaseConnection).where(
                        and_(
                            DatabaseConnection.is_active == True,
                            or_(
                                DatabaseConnection.user_id == user_id,
                                DatabaseConnection.is_shared == True
                            )
                        )
                    )
                
                result = await session.execute(stmt)
                connections = result.scalars().all()
                
                connection_ids = [conn.id for conn in connections]
                
                logger.debug(
                    "접근 가능한 연결 조회됨",
                    user_id=user_id,
                    connection_count=len(connection_ids),
                    user_role=user.role
                )
                
                return connection_ids
                
            except Exception as e:
                logger.error(
                    "접근 가능한 연결 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                return []
    
    async def can_upload_files(self, user_id: str) -> bool:
        """
        사용자가 파일을 업로드할 수 있는지 확인
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            파일 업로드 권한 여부
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user or not user.is_active:
                    return False
                
                # 모든 활성 사용자는 파일 업로드 가능 (추후 세분화 가능)
                has_permission = user.role in ["user", "admin", "analyst"]
                
                logger.debug(
                    "파일 업로드 권한 확인",
                    user_id=user_id,
                    has_permission=has_permission,
                    user_role=user.role
                )
                
                return has_permission
                
            except Exception as e:
                logger.error(
                    "파일 업로드 권한 확인 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                return False
    
    async def get_user_limits(self, user_id: str) -> Dict[str, Any]:
        """
        사용자별 제한사항 조회
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            사용자 제한사항 딕셔너리
        """
        async with self._session_factory() as session:
            try:
                user = await self._get_user_by_id(session, user_id)
                
                if not user:
                    return self._get_default_limits()
                
                # 역할별 제한사항 설정
                if user.role == "admin":
                    limits = {
                        "max_queries_per_hour": 1000,
                        "max_file_size_mb": 500,
                        "max_query_execution_time_seconds": 300,
                        "can_create_connections": True,
                        "can_share_connections": True
                    }
                elif user.role == "analyst":
                    limits = {
                        "max_queries_per_hour": 200,
                        "max_file_size_mb": 100,
                        "max_query_execution_time_seconds": 120,
                        "can_create_connections": True,
                        "can_share_connections": False
                    }
                else:  # user
                    limits = {
                        "max_queries_per_hour": 50,
                        "max_file_size_mb": 50,
                        "max_query_execution_time_seconds": 60,
                        "can_create_connections": False,
                        "can_share_connections": False
                    }
                
                logger.debug(
                    "사용자 제한사항 조회됨",
                    user_id=user_id,
                    user_role=user.role,
                    limits=limits
                )
                
                return limits
                
            except Exception as e:
                logger.error(
                    "사용자 제한사항 조회 실패",
                    user_id=user_id,
                    error=str(e),
                    exc_info=True
                )
                return self._get_default_limits()
    
    async def _get_user_by_id(self, session: AsyncSession, user_id: str) -> Optional[User]:
        """사용자 ID로 사용자 조회"""
        try:
            user = await session.get(User, user_id)
            return user
        except Exception as e:
            logger.error(f"사용자 조회 실패: {str(e)}")
            return None
    
    async def _get_connection_by_id(
        self, 
        session: AsyncSession, 
        connection_id: str
    ) -> Optional[DatabaseConnection]:
        """연결 ID로 데이터베이스 연결 조회"""
        try:
            connection = await session.get(DatabaseConnection, connection_id)
            return connection
        except Exception as e:
            logger.error(f"연결 조회 실패: {str(e)}")
            return None
    
    def _check_analysis_permission(self, user: User) -> bool:
        """분석 실행 권한 확인"""
        # 역할 기반 권한 확인
        allowed_roles = ["user", "analyst", "admin"]
        return user.role in allowed_roles and user.is_active
    
    def _check_connection_permission(self, user: User, connection: DatabaseConnection) -> bool:
        """연결 접근 권한 확인 (추후 확장 가능)"""
        # 현재는 소유자이거나 공유된 연결만 허용
        # 추후 그룹 기반 권한, 세분화된 권한 등으로 확장 가능
        return False
    
    def _get_default_limits(self) -> Dict[str, Any]:
        """기본 제한사항 반환"""
        return {
            "max_queries_per_hour": 10,
            "max_file_size_mb": 10,
            "max_query_execution_time_seconds": 30,
            "can_create_connections": False,
            "can_share_connections": False
        }
