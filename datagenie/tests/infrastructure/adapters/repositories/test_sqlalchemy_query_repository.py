"""
SQLAlchemy Query Repository Tests

실제 데이터베이스 기반 쿼리 저장소 테스트
TDD 규칙 준수: Infrastructure Layer 테스트
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.analysis_query import AnalysisQuery, QueryType, QueryStatus
from app.infrastructure.adapters.repositories.sqlalchemy_query_repository import SQLAlchemyQueryRepository
from app.models.query_history import QueryHistory


class TestSQLAlchemyQueryRepository:
    """SQLAlchemy 쿼리 저장소 테스트"""
    
    @pytest.fixture
    def mock_session_factory(self):
        """Mock 세션 팩토리"""
        session = AsyncMock(spec=AsyncSession)
        session_factory = AsyncMock()
        session_factory.return_value.__aenter__.return_value = session
        session_factory.return_value.__aexit__.return_value = None
        return session_factory, session
    
    @pytest.fixture
    def repository(self, mock_session_factory):
        """테스트용 저장소"""
        session_factory, _ = mock_session_factory
        return SQLAlchemyQueryRepository(session_factory)
    
    @pytest.fixture
    def sample_query(self):
        """테스트용 샘플 쿼리"""
        return AnalysisQuery.create_new(
            id="test-query-123",
            question="지난 3개월 매출 추이를 보여주세요",
            user_id="user-123",
            created_at=datetime.now(timezone.utc),
            connection_id="conn-123"
        )
    
    @pytest.mark.asyncio
    async def test_save_new_query(self, repository, mock_session_factory, sample_query):
        """RED → GREEN: 새 쿼리 저장"""
        # Arrange
        session_factory, session = mock_session_factory
        session.get.return_value = None  # 기존 쿼리 없음
        
        # Act
        await repository.save(sample_query)
        
        # Assert
        session.get.assert_called_once_with(QueryHistory, sample_query.id)
        session.add.assert_called_once()
        session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_save_existing_query(self, repository, mock_session_factory, sample_query):
        """RED → GREEN: 기존 쿼리 업데이트"""
        # Arrange
        session_factory, session = mock_session_factory
        existing_query = MagicMock(spec=QueryHistory)
        session.get.return_value = existing_query
        
        # Act
        await repository.save(sample_query)
        
        # Assert
        session.get.assert_called_once_with(QueryHistory, sample_query.id)
        assert existing_query.question == sample_query.question
        assert existing_query.status == sample_query.status.value
        session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_find_by_id_existing(self, repository, mock_session_factory):
        """RED → GREEN: ID로 기존 쿼리 조회"""
        # Arrange
        session_factory, session = mock_session_factory
        db_query = MagicMock(spec=QueryHistory)
        db_query.id = "test-query-123"
        db_query.user_id = "user-123"
        db_query.question = "테스트 질문"
        db_query.query_type = "database"
        db_query.status = "completed"
        db_query.connection_id = "conn-123"
        db_query.execution_time_ms = 1000
        db_query.error_message = None
        db_query.created_at = datetime.now(timezone.utc)
        db_query.updated_at = datetime.now(timezone.utc)
        
        session.get.return_value = db_query
        
        # Act
        result = await repository.find_by_id("test-query-123")
        
        # Assert
        assert result is not None
        assert result.id == "test-query-123"
        assert result.user_id == "user-123"
        assert result.question == "테스트 질문"
        session.get.assert_called_once_with(QueryHistory, "test-query-123")
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self, repository, mock_session_factory):
        """RED → GREEN: ID로 존재하지 않는 쿼리 조회"""
        # Arrange
        session_factory, session = mock_session_factory
        session.get.return_value = None
        
        # Act
        result = await repository.find_by_id("non-existent-id")
        
        # Assert
        assert result is None
        session.get.assert_called_once_with(QueryHistory, "non-existent-id")
    
    @pytest.mark.asyncio
    async def test_find_by_user_id(self, repository, mock_session_factory):
        """RED → GREEN: 사용자 ID로 쿼리 목록 조회"""
        # Arrange
        session_factory, session = mock_session_factory
        
        # Mock 쿼리 결과
        db_queries = [
            MagicMock(spec=QueryHistory),
            MagicMock(spec=QueryHistory)
        ]
        
        for i, db_query in enumerate(db_queries):
            db_query.id = f"query-{i}"
            db_query.user_id = "user-123"
            db_query.question = f"질문 {i}"
            db_query.query_type = "database"
            db_query.status = "completed"
            db_query.connection_id = "conn-123"
            db_query.execution_time_ms = 1000
            db_query.error_message = None
            db_query.created_at = datetime.now(timezone.utc)
            db_query.updated_at = datetime.now(timezone.utc)
        
        # Mock SQLAlchemy 결과
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = db_queries
        session.execute.return_value = mock_result
        
        # Act
        result = await repository.find_by_user_id("user-123", limit=10, offset=0)
        
        # Assert
        assert len(result) == 2
        assert all(query.user_id == "user-123" for query in result)
        session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_by_id_existing(self, repository, mock_session_factory):
        """RED → GREEN: 기존 쿼리 삭제"""
        # Arrange
        session_factory, session = mock_session_factory
        db_query = MagicMock(spec=QueryHistory)
        session.get.return_value = db_query
        
        # Act
        result = await repository.delete_by_id("test-query-123")
        
        # Assert
        assert result is True
        session.get.assert_called_once_with(QueryHistory, "test-query-123")
        session.delete.assert_called_once_with(db_query)
        session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, repository, mock_session_factory):
        """RED → GREEN: 존재하지 않는 쿼리 삭제"""
        # Arrange
        session_factory, session = mock_session_factory
        session.get.return_value = None
        
        # Act
        result = await repository.delete_by_id("non-existent-id")
        
        # Assert
        assert result is False
        session.get.assert_called_once_with(QueryHistory, "non-existent-id")
        session.delete.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_save_rollback_on_error(self, repository, mock_session_factory, sample_query):
        """RED → GREEN: 저장 실패시 롤백"""
        # Arrange
        session_factory, session = mock_session_factory
        session.get.return_value = None
        session.commit.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception):
            await repository.save(sample_query)
        
        session.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_count_by_user_id(self, repository, mock_session_factory):
        """RED → GREEN: 사용자별 쿼리 수 조회"""
        # Arrange
        session_factory, session = mock_session_factory
        
        # Mock 쿼리 결과
        db_queries = [MagicMock(spec=QueryHistory) for _ in range(5)]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = db_queries
        session.execute.return_value = mock_result
        
        # Act
        count = await repository.count_by_user_id("user-123")
        
        # Assert
        assert count == 5
        session.execute.assert_called_once()
    
    def test_to_domain_entity(self, repository):
        """RED → GREEN: 데이터베이스 모델을 도메인 엔티티로 변환"""
        # Arrange
        db_query = MagicMock(spec=QueryHistory)
        db_query.id = "test-query-123"
        db_query.user_id = "user-123"
        db_query.question = "테스트 질문"
        db_query.query_type = "database"
        db_query.status = "completed"
        db_query.connection_id = "conn-123"
        db_query.execution_time_ms = 1000
        db_query.error_message = None
        db_query.created_at = datetime.now(timezone.utc)
        db_query.updated_at = datetime.now(timezone.utc)
        
        # Act
        domain_query = repository._to_domain_entity(db_query)
        
        # Assert
        assert isinstance(domain_query, AnalysisQuery)
        assert domain_query.id == "test-query-123"
        assert domain_query.user_id == "user-123"
        assert domain_query.question == "테스트 질문"
        assert domain_query.query_type == QueryType.DATABASE
        assert domain_query.status == QueryStatus.COMPLETED
