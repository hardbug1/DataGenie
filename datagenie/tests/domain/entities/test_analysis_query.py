"""
AnalysisQuery Domain Entity Tests

TDD 규칙 준수: Domain 엔티티 테스트
"""

import pytest
from datetime import datetime, timezone
from app.domain.entities.analysis_query import AnalysisQuery, QueryType, QueryStatus


class TestAnalysisQuery:
    """AnalysisQuery 도메인 엔티티 테스트"""
    
    def test_create_valid_analysis_query(self):
        """RED → GREEN: 유효한 분석 쿼리 생성"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-123",
            question="지난 3개월 매출 추이를 보여주세요",
            user_id="user-123",
            created_at=datetime.now(timezone.utc),
            connection_id="conn-123"
        )
        
        # Assert
        assert query.is_valid() == True
        assert query.question == "지난 3개월 매출 추이를 보여주세요"
        assert query.user_id == "user-123"
        assert query.status == QueryStatus.PENDING
        assert query.can_be_executed_by("user-123") == True
        assert query.connection_id == "conn-123"
    
    def test_create_query_without_connection_id(self):
        """RED → GREEN: 연결 ID 없이 쿼리 생성"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-456",
            question="일반적인 데이터 분석 질문",
            user_id="user-456",
            created_at=datetime.now(timezone.utc)
        )
        
        # Assert
        assert query.is_valid() == True
        assert query.connection_id is None
        assert query.query_type == QueryType.GENERAL  # 연결 ID 없으면 일반 쿼리
    
    def test_invalid_query_empty_question(self):
        """RED → GREEN: 빈 질문 검증"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-empty",
            question="",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Assert
        assert query.is_valid() == False
    
    def test_invalid_query_whitespace_only_question(self):
        """RED → GREEN: 공백만 있는 질문 검증"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-whitespace",
            question="   \n\t   ",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Assert
        assert query.is_valid() == False
    
    def test_invalid_query_too_long(self):
        """RED → GREEN: 너무 긴 질문 검증"""
        # Arrange
        long_question = "A" * 1001  # 1000자 초과
        
        # Act
        query = AnalysisQuery.create_new(
            id="test-query-long",
            question=long_question,
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Assert
        assert query.is_valid() == False
    
    @pytest.mark.parametrize("user_id,expected", [
        ("user-123", True),   # 같은 사용자
        ("user-456", False),  # 다른 사용자
        ("", False),          # 빈 사용자 ID
    ])
    def test_execution_permission(self, user_id, expected):
        """RED → GREEN: 실행 권한 검증"""
        # Arrange
        query = AnalysisQuery.create_new(
            id="test-query-perm",
            question="테스트 질문",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Act & Assert
        assert query.can_be_executed_by(user_id) == expected
    
    def test_query_type_determination_with_connection(self):
        """RED → GREEN: 연결 ID가 있을 때 쿼리 타입 결정"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-db",
            question="SELECT * FROM users",
            user_id="user-123",
            created_at=datetime.now(timezone.utc),
            connection_id="db-conn-123"
        )
        
        # Assert
        assert query.query_type == QueryType.DATABASE
    
    def test_query_type_determination_excel_keywords(self):
        """RED → GREEN: Excel 키워드가 있을 때 쿼리 타입 결정"""
        # Arrange & Act
        query = AnalysisQuery.create_new(
            id="test-query-excel",
            question="엑셀 파일의 데이터를 분석해주세요",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Assert
        assert query.query_type == QueryType.EXCEL
    
    def test_query_immutability(self):
        """RED → GREEN: 쿼리 불변성 확인"""
        # Arrange
        query = AnalysisQuery.create_new(
            id="test-query-immutable",
            question="불변성 테스트",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Act & Assert
        with pytest.raises(AttributeError):
            query.question = "변경된 질문"  # frozen=True로 인해 변경 불가
    
    def test_query_status_progression(self):
        """RED → GREEN: 쿼리 상태 변경"""
        # Arrange
        original_query = AnalysisQuery.create_new(
            id="test-query-status",
            question="상태 변경 테스트",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Act
        processing_query = original_query.with_status(QueryStatus.PROCESSING)
        completed_query = processing_query.with_status(
            QueryStatus.COMPLETED,
            execution_time_ms=1500
        )
        
        # Assert
        assert original_query.status == QueryStatus.PENDING
        assert processing_query.status == QueryStatus.PROCESSING
        assert completed_query.status == QueryStatus.COMPLETED
        assert completed_query.execution_time_ms == 1500
    
    def test_query_with_error(self):
        """RED → GREEN: 에러가 있는 쿼리 상태"""
        # Arrange
        query = AnalysisQuery.create_new(
            id="test-query-error",
            question="에러 테스트",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Act
        error_query = query.with_status(
            QueryStatus.FAILED,
            error_message="테스트 에러 메시지"
        )
        
        # Assert
        assert error_query.status == QueryStatus.FAILED
        assert error_query.error_message == "테스트 에러 메시지"
        assert error_query.has_error() == True
    
    def test_query_string_representation(self):
        """RED → GREEN: 쿼리 문자열 표현"""
        # Arrange
        query = AnalysisQuery.create_new(
            id="test-query-str",
            question="문자열 표현 테스트",
            user_id="user-123",
            created_at=datetime.now(timezone.utc)
        )
        
        # Act
        query_str = str(query)
        
        # Assert
        assert "test-query-str" in query_str
        assert "문자열 표현 테스트" in query_str
        assert "user-123" in query_str
