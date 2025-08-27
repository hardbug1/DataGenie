"""
Analysis Query Domain Entity

Clean Architecture: 도메인 엔티티
- 비즈니스 규칙을 캡슐화
- 외부 의존성 없음
- 불변성과 일관성 보장
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class QueryType(Enum):
    """쿼리 유형"""
    DATABASE = "database"
    EXCEL = "excel"
    GENERAL = "general"


class QueryStatus(Enum):
    """쿼리 상태"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class AnalysisQuery:
    """
    분석 쿼리 도메인 엔티티
    
    Clean Architecture: 이 엔티티는 분석 쿼리의 핵심 비즈니스 규칙을 담당합니다.
    - 불변 객체 (frozen=True)
    - 비즈니스 규칙 검증
    - 상태 변경 메서드
    """
    
    id: str
    question: str
    user_id: str
    query_type: QueryType
    status: QueryStatus
    created_at: datetime
    connection_id: Optional[str] = None
    execution_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    
    @classmethod
    def create_new(
        cls,
        id: str,
        question: str,
        user_id: str,
        created_at: datetime,
        connection_id: Optional[str] = None
    ) -> "AnalysisQuery":
        """
        새로운 분석 쿼리 생성 팩토리 메서드
        
        Args:
            id: 쿼리 고유 식별자
            question: 사용자 질문
            user_id: 사용자 ID
            created_at: 생성 시간
            connection_id: 데이터베이스 연결 ID (선택사항)
            
        Returns:
            새로운 AnalysisQuery 인스턴스
        """
        # 질문 유형 자동 결정 (간단한 휴리스틱)
        query_type = cls._determine_query_type(question, connection_id)
        
        return cls(
            id=id,
            question=question,
            user_id=user_id,
            query_type=query_type,
            status=QueryStatus.PENDING,
            created_at=created_at,
            connection_id=connection_id
        )
    
    def is_valid(self) -> bool:
        """
        비즈니스 규칙 검증
        
        Returns:
            bool: 쿼리가 유효한지 여부
        """
        # 비즈니스 규칙 1: 질문이 비어있지 않아야 함
        if not self.question or not self.question.strip():
            return False
        
        # 비즈니스 규칙 2: 질문 길이 제한 (1000자)
        if len(self.question.strip()) > 1000:
            return False
        
        # 비즈니스 규칙 3: 사용자 ID가 있어야 함
        if not self.user_id or not self.user_id.strip():
            return False
        
        # 비즈니스 규칙 4: 데이터베이스 쿼리인 경우 연결 ID 필요
        if self.query_type == QueryType.DATABASE and not self.connection_id:
            return False
        
        return True
    
    def can_be_executed_by(self, user_id: str) -> bool:
        """
        특정 사용자가 이 쿼리를 실행할 수 있는지 확인
        
        Args:
            user_id: 확인할 사용자 ID
            
        Returns:
            bool: 실행 가능 여부
        """
        return self.user_id == user_id and user_id.strip() != ""
    
    def with_status(
        self, 
        new_status: QueryStatus, 
        execution_time_ms: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> "AnalysisQuery":
        """
        상태가 변경된 새로운 쿼리 인스턴스 생성
        
        Args:
            new_status: 새로운 상태
            execution_time_ms: 실행 시간 (밀리초)
            error_message: 에러 메시지
            
        Returns:
            AnalysisQuery: 상태가 변경된 새 인스턴스
        """
        return AnalysisQuery(
            id=self.id,
            question=self.question,
            user_id=self.user_id,
            query_type=self.query_type,
            status=new_status,
            created_at=self.created_at,
            connection_id=self.connection_id,
            execution_time_ms=execution_time_ms or self.execution_time_ms,
            error_message=error_message or self.error_message
        )
    
    def has_error(self) -> bool:
        """에러가 있는지 확인"""
        return self.status == QueryStatus.FAILED and self.error_message is not None
    
    def __str__(self) -> str:
        """문자열 표현"""
        return f"AnalysisQuery(id={self.id}, question='{self.question[:50]}...', user_id={self.user_id}, status={self.status.value})"
    
    def is_processing(self) -> bool:
        """쿼리가 처리 중인지 확인"""
        return self.status == QueryStatus.PROCESSING
    
    def is_completed(self) -> bool:
        """쿼리가 완료되었는지 확인"""
        return self.status == QueryStatus.COMPLETED
    
    def is_failed(self) -> bool:
        """쿼리가 실패했는지 확인"""
        return self.status == QueryStatus.FAILED
    
    def mark_processing(self) -> "AnalysisQuery":
        """
        쿼리를 처리 중 상태로 변경
        
        Returns:
            새로운 AnalysisQuery 인스턴스 (불변 객체)
        """
        if self.status != QueryStatus.PENDING:
            raise InvalidStateTransitionError(
                f"PENDING 상태에서만 PROCESSING으로 변경 가능. 현재 상태: {self.status}"
            )
        
        return self._replace(status=QueryStatus.PROCESSING)
    
    def mark_completed(self, execution_time_ms: int) -> "AnalysisQuery":
        """
        쿼리를 완료 상태로 변경
        
        Args:
            execution_time_ms: 실행 시간 (밀리초)
            
        Returns:
            새로운 AnalysisQuery 인스턴스
        """
        if self.status not in [QueryStatus.PENDING, QueryStatus.PROCESSING]:
            raise InvalidStateTransitionError(
                f"PENDING 또는 PROCESSING 상태에서만 COMPLETED로 변경 가능. 현재 상태: {self.status}"
            )
        
        if execution_time_ms < 0:
            raise ValueError("실행 시간은 0 이상이어야 합니다")
        
        return self._replace(
            status=QueryStatus.COMPLETED,
            execution_time_ms=execution_time_ms
        )
    
    def mark_failed(self, error_message: str, execution_time_ms: int) -> "AnalysisQuery":
        """
        쿼리를 실패 상태로 변경
        
        Args:
            error_message: 오류 메시지
            execution_time_ms: 실행 시간 (밀리초)
            
        Returns:
            새로운 AnalysisQuery 인스턴스
        """
        if not error_message or not error_message.strip():
            raise ValueError("오류 메시지는 비어있을 수 없습니다")
        
        if execution_time_ms < 0:
            raise ValueError("실행 시간은 0 이상이어야 합니다")
        
        return self._replace(
            status=QueryStatus.FAILED,
            error_message=error_message.strip(),
            execution_time_ms=execution_time_ms
        )
    
    def get_execution_duration_seconds(self) -> Optional[float]:
        """
        실행 시간을 초 단위로 반환
        
        Returns:
            실행 시간 (초) 또는 None
        """
        if self.execution_time_ms is None:
            return None
        return self.execution_time_ms / 1000.0
    
    @staticmethod
    def _determine_query_type(question: str, connection_id: Optional[str]) -> QueryType:
        """
        질문과 컨텍스트를 기반으로 쿼리 유형 결정
        
        Args:
            question: 사용자 질문
            connection_id: 데이터베이스 연결 ID
            
        Returns:
            QueryType: 결정된 쿼리 유형
        """
        question_lower = question.lower().strip()
        
        # 데이터베이스 관련 키워드 확인
        db_keywords = [
            "매출", "고객", "주문", "상품", "데이터베이스", "테이블", "조회",
            "sales", "customer", "order", "product", "database", "table", "select"
        ]
        
        # Excel 관련 키워드 확인
        excel_keywords = [
            "파일", "엑셀", "업로드", "분석", "차트", "그래프",
            "file", "excel", "upload", "analyze", "chart", "graph"
        ]
        
        # 연결 ID가 있으면 데이터베이스 쿼리로 우선 분류
        if connection_id:
            return QueryType.DATABASE
        
        # 키워드 기반 분류
        if any(keyword in question_lower for keyword in db_keywords):
            return QueryType.DATABASE
        elif any(keyword in question_lower for keyword in excel_keywords):
            return QueryType.EXCEL
        else:
            return QueryType.GENERAL
    
    def _replace(self, **changes) -> "AnalysisQuery":
        """
        불변 객체의 일부 필드를 변경한 새 인스턴스 생성
        
        Args:
            **changes: 변경할 필드들
            
        Returns:
            새로운 AnalysisQuery 인스턴스
        """
        # dataclass의 replace 기능 구현
        current_values = {
            'id': self.id,
            'question': self.question,
            'user_id': self.user_id,
            'query_type': self.query_type,
            'status': self.status,
            'created_at': self.created_at,
            'connection_id': self.connection_id,
            'execution_time_ms': self.execution_time_ms,
            'error_message': self.error_message
        }
        
        current_values.update(changes)
        return AnalysisQuery(**current_values)


class InvalidStateTransitionError(Exception):
    """잘못된 상태 전환 예외"""
    pass
