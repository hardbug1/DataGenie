"""
SQL Security Validator

Clean Architecture: Application Core
SQL 인젝션 방지 및 안전한 쿼리 검증을 담당하는 핵심 보안 컴포넌트
"""

import re
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import structlog

logger = structlog.get_logger(__name__)


class SecurityThreatLevel(Enum):
    """보안 위협 수준"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class SQLValidationResult:
    """SQL 검증 결과"""
    is_safe: bool
    threat_level: SecurityThreatLevel
    violations: List[str]
    sanitized_sql: Optional[str] = None
    warnings: List[str] = None
    
    def has_violations(self) -> bool:
        """위반 사항이 있는지 확인"""
        return len(self.violations) > 0
    
    def is_execution_allowed(self) -> bool:
        """실행 허용 여부"""
        return self.is_safe and self.threat_level != SecurityThreatLevel.CRITICAL


class SQLSecurityValidator:
    """
    SQL 보안 검증기
    
    Database Security 규칙 준수:
    - SQL 인젝션 방지
    - 위험한 SQL 연산 차단
    - 읽기 전용 쿼리만 허용
    """
    
    # 절대 금지된 SQL 키워드 (Database Security 규칙)
    FORBIDDEN_SQL_KEYWORDS = [
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER",
        "TRUNCATE", "EXEC", "EXECUTE", "CALL", "GRANT", "REVOKE",
        "COMMIT", "ROLLBACK", "SAVEPOINT", "MERGE", "REPLACE",
        "RENAME", "COMMENT", "LOCK", "UNLOCK"
    ]
    
    # 위험한 SQL 패턴 (Database Security 규칙)
    DANGEROUS_SQL_PATTERNS = [
        r'\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE)\b',
        r'\b(EXEC|EXECUTE|CALL)\b',
        r';\s*(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)',
        r'--',  # SQL 주석
        r'/\*.*?\*/',  # 다중 라인 주석
        r'\bUNION\s+SELECT\b',  # UNION 기반 인젝션
        r'\bOR\s+1\s*=\s*1\b',  # 항상 참인 조건
        r'\bAND\s+1\s*=\s*1\b',  # 항상 참인 조건
        r"'.*?OR.*?'.*?=.*?'",  # 문자열 기반 인젝션
        r'\bSLEEP\s*\(',  # 시간 지연 공격
        r'\bBENCHMARK\s*\(',  # 벤치마크 공격
        r'\bLOAD_FILE\s*\(',  # 파일 읽기 공격
        r'\bINTO\s+OUTFILE\b',  # 파일 쓰기 공격
        r'\bINTO\s+DUMPFILE\b',  # 덤프 파일 공격
    ]
    
    # 의심스러운 패턴 (경고 수준)
    SUSPICIOUS_PATTERNS = [
        r'\bSELECT\s+\*\s+FROM\s+\w+\s*;?\s*--',  # 주석과 함께하는 전체 선택
        r'\bSELECT\s+COUNT\s*\(\s*\*\s*\)\s+FROM\s+information_schema',  # 스키마 정보 조회
        r'\bSELECT\s+.*\s+FROM\s+mysql\.',  # MySQL 시스템 테이블 접근
        r'\bSELECT\s+.*\s+FROM\s+pg_',  # PostgreSQL 시스템 테이블 접근
        r'\bSELECT\s+.*\s+FROM\s+sys\.',  # 시스템 테이블 접근
    ]
    
    def __init__(self):
        """SQL 보안 검증기 초기화"""
        self._compiled_dangerous_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self.DANGEROUS_SQL_PATTERNS
        ]
        self._compiled_suspicious_patterns = [
            re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for pattern in self.SUSPICIOUS_PATTERNS
        ]
    
    def validate_sql(self, sql: str, context: Optional[Dict[str, Any]] = None) -> SQLValidationResult:
        """
        SQL 쿼리 보안 검증
        
        Args:
            sql: 검증할 SQL 쿼리
            context: 추가 컨텍스트 정보 (사용자 ID, 연결 정보 등)
            
        Returns:
            SQLValidationResult: 검증 결과
        """
        if not sql or not sql.strip():
            return SQLValidationResult(
                is_safe=False,
                threat_level=SecurityThreatLevel.HIGH,
                violations=["빈 SQL 쿼리는 허용되지 않습니다"]
            )
        
        violations = []
        warnings = []
        threat_level = SecurityThreatLevel.LOW
        
        # 1. 금지된 키워드 검사
        keyword_violations = self._check_forbidden_keywords(sql)
        if keyword_violations:
            violations.extend(keyword_violations)
            threat_level = SecurityThreatLevel.CRITICAL
        
        # 2. 위험한 패턴 검사
        pattern_violations = self._check_dangerous_patterns(sql)
        if pattern_violations:
            violations.extend(pattern_violations)
            if threat_level != SecurityThreatLevel.CRITICAL:
                threat_level = SecurityThreatLevel.HIGH
        
        # 3. 의심스러운 패턴 검사 (경고)
        suspicious_warnings = self._check_suspicious_patterns(sql)
        if suspicious_warnings:
            warnings.extend(suspicious_warnings)
            if threat_level == SecurityThreatLevel.LOW:
                threat_level = SecurityThreatLevel.MEDIUM
        
        # 4. SELECT 문인지 확인
        if not self._is_select_query(sql):
            violations.append("SELECT 쿼리만 허용됩니다")
            threat_level = SecurityThreatLevel.CRITICAL
        
        # 5. 쿼리 길이 검사
        if len(sql) > 10000:  # 10KB 제한
            violations.append("쿼리가 너무 깁니다 (최대 10KB)")
            threat_level = SecurityThreatLevel.HIGH
        
        # 6. LIMIT 절 확인 및 추가
        sanitized_sql = self._ensure_limit_clause(sql) if not violations else None
        
        # 보안 이벤트 로깅
        self._log_security_event(sql, violations, warnings, context)
        
        return SQLValidationResult(
            is_safe=len(violations) == 0,
            threat_level=threat_level,
            violations=violations,
            sanitized_sql=sanitized_sql,
            warnings=warnings
        )
    
    def _check_forbidden_keywords(self, sql: str) -> List[str]:
        """금지된 키워드 검사"""
        violations = []
        sql_upper = sql.upper()
        
        for keyword in self.FORBIDDEN_SQL_KEYWORDS:
            # 단어 경계를 고려한 정확한 매칭
            pattern = rf'\b{re.escape(keyword)}\b'
            if re.search(pattern, sql_upper):
                violations.append(f"금지된 SQL 키워드 감지: {keyword}")
        
        return violations
    
    def _check_dangerous_patterns(self, sql: str) -> List[str]:
        """위험한 패턴 검사"""
        violations = []
        
        for i, pattern in enumerate(self._compiled_dangerous_patterns):
            if pattern.search(sql):
                violations.append(f"위험한 SQL 패턴 감지: {self.DANGEROUS_SQL_PATTERNS[i]}")
        
        return violations
    
    def _check_suspicious_patterns(self, sql: str) -> List[str]:
        """의심스러운 패턴 검사"""
        warnings = []
        
        for i, pattern in enumerate(self._compiled_suspicious_patterns):
            if pattern.search(sql):
                warnings.append(f"의심스러운 SQL 패턴: {self.SUSPICIOUS_PATTERNS[i]}")
        
        return warnings
    
    def _is_select_query(self, sql: str) -> bool:
        """SELECT 쿼리인지 확인"""
        # 공백과 주석을 제거한 후 첫 번째 토큰 확인
        cleaned_sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)  # 다중 라인 주석 제거
        cleaned_sql = re.sub(r'--.*$', '', cleaned_sql, flags=re.MULTILINE)  # 단일 라인 주석 제거
        cleaned_sql = cleaned_sql.strip()
        
        if not cleaned_sql:
            return False
        
        # 첫 번째 단어가 SELECT인지 확인
        first_word = cleaned_sql.split()[0].upper()
        return first_word == "SELECT"
    
    def _ensure_limit_clause(self, sql: str) -> str:
        """LIMIT 절 확인 및 추가"""
        sql_upper = sql.upper()
        
        # 이미 LIMIT이 있는지 확인
        if 'LIMIT' in sql_upper:
            return sql
        
        # LIMIT 절 추가 (최대 1000행)
        sql = sql.rstrip().rstrip(';')
        return f"{sql} LIMIT 1000"
    
    def _log_security_event(
        self, 
        sql: str, 
        violations: List[str], 
        warnings: List[str],
        context: Optional[Dict[str, Any]]
    ):
        """보안 이벤트 로깅"""
        sql_hash = hashlib.sha256(sql.encode()).hexdigest()[:16]
        
        if violations:
            logger.error(
                "SQL 보안 위반 감지",
                extra={
                    "sql_hash": sql_hash,
                    "violations": violations,
                    "threat_level": "HIGH" if violations else "MEDIUM",
                    "user_id": context.get("user_id") if context else None,
                    "connection_id": context.get("connection_id") if context else None
                }
            )
        elif warnings:
            logger.warning(
                "의심스러운 SQL 패턴 감지",
                extra={
                    "sql_hash": sql_hash,
                    "warnings": warnings,
                    "user_id": context.get("user_id") if context else None,
                    "connection_id": context.get("connection_id") if context else None
                }
            )
        else:
            logger.info(
                "SQL 보안 검증 통과",
                extra={
                    "sql_hash": sql_hash,
                    "user_id": context.get("user_id") if context else None,
                    "connection_id": context.get("connection_id") if context else None
                }
            )


class SecurityError(Exception):
    """보안 관련 예외"""
    
    def __init__(self, message: str, threat_level: SecurityThreatLevel = SecurityThreatLevel.HIGH):
        super().__init__(message)
        self.threat_level = threat_level


class SQLInjectionError(SecurityError):
    """SQL 인젝션 관련 예외"""
    
    def __init__(self, message: str, violations: List[str]):
        super().__init__(message, SecurityThreatLevel.CRITICAL)
        self.violations = violations
