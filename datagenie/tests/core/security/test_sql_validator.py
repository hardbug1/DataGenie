"""
SQL Security Validator Tests

TDD 규칙 준수: 보안 시스템 테스트
"""

import pytest
from app.core.security.sql_validator import (
    SQLSecurityValidator,
    SQLValidationResult,
    SecurityThreatLevel,
    SecurityError,
    SQLInjectionError
)


class TestSQLSecurityValidator:
    """SQL 보안 검증기 테스트"""
    
    @pytest.fixture
    def validator(self):
        """SQL 검증기 픽스처"""
        return SQLSecurityValidator()
    
    def test_valid_select_query(self, validator):
        """RED → GREEN: 유효한 SELECT 쿼리 검증"""
        # Arrange
        safe_sql = "SELECT id, name FROM users WHERE age > 18"
        
        # Act
        result = validator.validate_sql(safe_sql)
        
        # Assert
        assert result.is_safe == True
        assert result.threat_level == SecurityThreatLevel.LOW
        assert len(result.violations) == 0
        assert result.is_execution_allowed() == True
        assert "LIMIT" in result.sanitized_sql  # 자동으로 LIMIT 추가
    
    def test_sql_with_existing_limit(self, validator):
        """RED → GREEN: 이미 LIMIT이 있는 쿼리"""
        # Arrange
        sql_with_limit = "SELECT * FROM products LIMIT 50"
        
        # Act
        result = validator.validate_sql(sql_with_limit)
        
        # Assert
        assert result.is_safe == True
        assert result.sanitized_sql == sql_with_limit  # LIMIT 추가 안 함
    
    @pytest.mark.parametrize("forbidden_keyword", [
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
        "TRUNCATE", "EXEC", "EXECUTE", "CALL", "GRANT", "REVOKE"
    ])
    def test_forbidden_sql_keywords(self, validator, forbidden_keyword):
        """RED → GREEN: 금지된 SQL 키워드 탐지"""
        # Arrange
        dangerous_sql = f"{forbidden_keyword} INTO users VALUES (1, 'test')"
        
        # Act
        result = validator.validate_sql(dangerous_sql)
        
        # Assert
        assert result.is_safe == False
        assert result.threat_level == SecurityThreatLevel.CRITICAL
        assert len(result.violations) > 0
        assert any(forbidden_keyword in violation for violation in result.violations)
        assert result.is_execution_allowed() == False
    
    def test_sql_injection_patterns(self, validator):
        """RED → GREEN: SQL 인젝션 패턴 탐지"""
        # Arrange
        injection_attempts = [
            "SELECT * FROM users WHERE id = 1 OR 1=1",
            "SELECT * FROM users; DROP TABLE users; --",
            "SELECT * FROM users UNION SELECT * FROM passwords",
            "SELECT * FROM users WHERE name = 'admin'--'",
            "SELECT SLEEP(10)"
        ]
        
        for sql in injection_attempts:
            # Act
            result = validator.validate_sql(sql)
            
            # Assert
            assert result.is_safe == False, f"Failed to detect injection in: {sql}"
            assert result.threat_level in [SecurityThreatLevel.HIGH, SecurityThreatLevel.CRITICAL]
            assert len(result.violations) > 0
    
    def test_non_select_query_rejection(self, validator):
        """RED → GREEN: SELECT가 아닌 쿼리 거부"""
        # Arrange
        non_select_queries = [
            "SHOW TABLES",
            "DESCRIBE users",
            "EXPLAIN SELECT * FROM users"
        ]
        
        for sql in non_select_queries:
            # Act
            result = validator.validate_sql(sql)
            
            # Assert
            assert result.is_safe == False, f"Should reject non-SELECT: {sql}"
            assert "SELECT 쿼리만 허용됩니다" in result.violations
    
    def test_empty_sql_validation(self, validator):
        """RED → GREEN: 빈 SQL 쿼리 검증"""
        # Arrange
        empty_queries = ["", "   ", "\n\t  ", None]
        
        for sql in empty_queries:
            # Act
            result = validator.validate_sql(sql)
            
            # Assert
            assert result.is_safe == False
            assert result.threat_level == SecurityThreatLevel.HIGH
            assert "빈 SQL 쿼리는 허용되지 않습니다" in result.violations
    
    def test_sql_length_limit(self, validator):
        """RED → GREEN: SQL 길이 제한 검증"""
        # Arrange
        very_long_sql = "SELECT * FROM users WHERE " + "id = 1 AND " * 1000 + "name = 'test'"
        
        # Act
        result = validator.validate_sql(very_long_sql)
        
        # Assert
        assert result.is_safe == False
        assert result.threat_level == SecurityThreatLevel.HIGH
        assert any("너무 깁니다" in violation for violation in result.violations)
    
    def test_suspicious_patterns_warning(self, validator):
        """RED → GREEN: 의심스러운 패턴 경고"""
        # Arrange
        suspicious_sql = "SELECT COUNT(*) FROM information_schema.tables"
        
        # Act
        result = validator.validate_sql(suspicious_sql)
        
        # Assert
        assert result.threat_level == SecurityThreatLevel.MEDIUM
        assert result.warnings is not None
        assert len(result.warnings) > 0
    
    def test_sql_comments_detection(self, validator):
        """RED → GREEN: SQL 주석 탐지"""
        # Arrange
        sql_with_comments = [
            "SELECT * FROM users -- comment",
            "SELECT * FROM users /* comment */",
            "SELECT * FROM users; -- DROP TABLE users"
        ]
        
        for sql in sql_with_comments:
            # Act
            result = validator.validate_sql(sql)
            
            # Assert
            assert result.is_safe == False, f"Should detect comment in: {sql}"
            assert result.threat_level in [SecurityThreatLevel.HIGH, SecurityThreatLevel.CRITICAL]
    
    def test_context_logging(self, validator):
        """RED → GREEN: 컨텍스트 정보 로깅"""
        # Arrange
        sql = "SELECT * FROM users"
        context = {
            "user_id": "test-user-123",
            "connection_id": "test-conn-456"
        }
        
        # Act
        result = validator.validate_sql(sql, context)
        
        # Assert
        assert result.is_safe == True
        # 로깅이 정상적으로 수행되었는지는 로그 출력으로 확인
    
    def test_case_insensitive_detection(self, validator):
        """RED → GREEN: 대소문자 구분 없는 탐지"""
        # Arrange
        mixed_case_sql = [
            "select * from users where id = 1 or 1=1",
            "Select * From Users; drop table users;",
            "SELECT * FROM users UnIoN sElEcT * FROM passwords"
        ]
        
        for sql in mixed_case_sql:
            # Act
            result = validator.validate_sql(sql)
            
            # Assert
            assert result.is_safe == False, f"Should detect mixed case: {sql}"
    
    def test_complex_valid_query(self, validator):
        """RED → GREEN: 복잡하지만 안전한 쿼리"""
        # Arrange
        complex_sql = """
        SELECT 
            u.id,
            u.username,
            COUNT(o.id) as order_count,
            SUM(o.amount) as total_amount
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.created_at >= '2023-01-01'
        GROUP BY u.id, u.username
        HAVING COUNT(o.id) > 0
        ORDER BY total_amount DESC
        """
        
        # Act
        result = validator.validate_sql(complex_sql)
        
        # Assert
        assert result.is_safe == True
        assert result.threat_level == SecurityThreatLevel.LOW
        assert "LIMIT" in result.sanitized_sql
    
    def test_validation_result_properties(self, validator):
        """RED → GREEN: 검증 결과 속성 테스트"""
        # Arrange
        safe_sql = "SELECT id FROM users"
        unsafe_sql = "DROP TABLE users"
        
        # Act
        safe_result = validator.validate_sql(safe_sql)
        unsafe_result = validator.validate_sql(unsafe_sql)
        
        # Assert
        # 안전한 쿼리
        assert safe_result.has_violations() == False
        assert safe_result.is_execution_allowed() == True
        
        # 위험한 쿼리
        assert unsafe_result.has_violations() == True
        assert unsafe_result.is_execution_allowed() == False
