"""
Pytest Configuration and Fixtures

DataGenie 전용 테스트 설정 및 공통 픽스처
"""

import pytest
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, AsyncGenerator
from unittest.mock import Mock, AsyncMock

from app.domain.entities.analysis_query import AnalysisQuery, QueryType, QueryStatus
from app.domain.value_objects.analysis_result import AnalysisResult
from app.core.auth.jwt_manager import JWTManager
from app.core.security.sql_validator import SQLSecurityValidator
from app.core.security.pii_masker import PIIMasker


@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 픽스처"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_analysis_query() -> AnalysisQuery:
    """샘플 분석 쿼리 픽스처"""
    return AnalysisQuery.create_new(
        id="test-query-123",
        question="지난 3개월 매출 추이를 보여주세요",
        user_id="test-user-123",
        created_at=datetime.now(timezone.utc),
        connection_id="test-conn-123"
    )


@pytest.fixture
def sample_analysis_result() -> AnalysisResult:
    """샘플 분석 결과 픽스처"""
    return AnalysisResult(
        analysis_type="database",
        question="테스트 질문",
        sql_query="SELECT * FROM test_table LIMIT 10",
        execution_success=True,
        data=[
            {"id": 1, "name": "테스트1", "value": 100},
            {"id": 2, "name": "테스트2", "value": 200}
        ],
        columns=["id", "name", "value"],
        row_count=2,
        summary="테스트 결과입니다"
    )


@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """테스트 사용자 데이터 픽스처"""
    return {
        "user_id": "test-user-123",
        "username": "testuser",
        "email": "test@example.com",
        "role": "user",
        "permissions": ["analysis:execute", "query:read"]
    }


@pytest.fixture
def admin_user_data() -> Dict[str, Any]:
    """관리자 사용자 데이터 픽스처"""
    return {
        "user_id": "admin-user-123",
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "permissions": [
            "analysis:execute",
            "query:read",
            "query:write",
            "user:manage",
            "connection:manage"
        ]
    }


@pytest.fixture
def jwt_manager() -> JWTManager:
    """JWT 관리자 픽스처"""
    return JWTManager(
        secret_key="test-secret-key-for-testing-only",
        access_token_expire_minutes=30,
        refresh_token_expire_days=7
    )


@pytest.fixture
def sql_validator() -> SQLSecurityValidator:
    """SQL 보안 검증기 픽스처"""
    return SQLSecurityValidator()


@pytest.fixture
def pii_masker() -> PIIMasker:
    """PII 마스킹 시스템 픽스처"""
    return PIIMasker(min_confidence=0.7)


@pytest.fixture
def mock_query_repository() -> AsyncMock:
    """Mock 쿼리 저장소 픽스처"""
    mock = AsyncMock()
    mock.save.return_value = None
    mock.find_by_id.return_value = None
    mock.find_by_user_id.return_value = []
    mock.update_status.return_value = None
    return mock


@pytest.fixture
def mock_analysis_engine() -> AsyncMock:
    """Mock 분석 엔진 픽스처"""
    mock = AsyncMock()
    mock.execute_analysis.return_value = AnalysisResult(
        analysis_type="database",
        question="Mock 질문",
        sql_query="SELECT 1",
        execution_success=True,
        data=[{"result": 1}],
        columns=["result"],
        row_count=1,
        summary="Mock 결과"
    )
    return mock


@pytest.fixture
def mock_user_permissions() -> AsyncMock:
    """Mock 사용자 권한 서비스 픽스처"""
    mock = AsyncMock()
    mock.can_execute_analysis.return_value = True
    mock.can_access_connection.return_value = True
    return mock


@pytest.fixture
def test_database_schema() -> Dict[str, Any]:
    """테스트 데이터베이스 스키마 픽스처"""
    return {
        "users": {
            "columns": [
                {"name": "id", "type": "integer", "primary_key": True},
                {"name": "username", "type": "varchar", "nullable": False},
                {"name": "email", "type": "varchar", "nullable": False},
                {"name": "created_at", "type": "timestamp", "nullable": False}
            ]
        },
        "orders": {
            "columns": [
                {"name": "id", "type": "integer", "primary_key": True},
                {"name": "user_id", "type": "integer", "foreign_key": "users.id"},
                {"name": "amount", "type": "decimal", "nullable": False},
                {"name": "status", "type": "varchar", "nullable": False},
                {"name": "created_at", "type": "timestamp", "nullable": False}
            ]
        },
        "products": {
            "columns": [
                {"name": "id", "type": "integer", "primary_key": True},
                {"name": "name", "type": "varchar", "nullable": False},
                {"name": "price", "type": "decimal", "nullable": False},
                {"name": "category", "type": "varchar", "nullable": True}
            ]
        }
    }


@pytest.fixture
def sample_pii_data() -> Dict[str, str]:
    """개인정보가 포함된 샘플 데이터 픽스처"""
    return {
        "email": "user@example.com",
        "phone": "010-1234-5678",
        "korean_rrn": "123456-1234567",
        "credit_card": "1234-5678-9012-3456",
        "mixed_text": "연락처: 010-9876-5432, 이메일: john.doe@company.com"
    }


class DataGenieTestHelpers:
    """DataGenie 전용 테스트 헬퍼 클래스"""
    
    @staticmethod
    def create_test_user(user_id: str = "test-user") -> Dict[str, Any]:
        """테스트 사용자 생성"""
        return {
            "user_id": user_id,
            "username": f"{user_id}_name",
            "email": f"{user_id}@test.com",
            "role": "user",
            "permissions": ["analysis:execute", "query:read"]
        }
    
    @staticmethod
    def assert_valid_analysis_result(result: AnalysisResult):
        """분석 결과 유효성 검증"""
        assert hasattr(result, 'analysis_type')
        assert hasattr(result, 'question')
        assert hasattr(result, 'execution_success')
        
        if result.execution_success:
            assert result.data is not None or result.sql_query is not None
    
    @staticmethod
    def assert_valid_jwt_token(token: str, jwt_manager: JWTManager):
        """JWT 토큰 유효성 검증"""
        validation_result = jwt_manager.validate_token(token)
        assert validation_result.is_valid
        assert validation_result.payload is not None
    
    @staticmethod
    def create_safe_sql_query(table_name: str = "users") -> str:
        """안전한 SQL 쿼리 생성"""
        return f"SELECT id, username FROM {table_name} WHERE id > 0 LIMIT 10"
    
    @staticmethod
    def create_unsafe_sql_query() -> str:
        """위험한 SQL 쿼리 생성 (테스트용)"""
        return "DROP TABLE users; --"


@pytest.fixture
def test_helpers() -> DataGenieTestHelpers:
    """테스트 헬퍼 픽스처"""
    return DataGenieTestHelpers()
