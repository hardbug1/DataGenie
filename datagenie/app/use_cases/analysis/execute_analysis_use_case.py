"""
Execute Analysis Use Case

자연어 질문을 받아 데이터 분석을 수행하는 핵심 Use Case
Clean Architecture: Application Business Rules
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Protocol
from dataclasses import dataclass

from app.domain.entities.analysis_query import AnalysisQuery, QueryType, QueryStatus
from app.domain.value_objects.analysis_result import AnalysisResult
from app.domain.interfaces.repositories.query_repository import IQueryRepository
from app.domain.interfaces.services.analysis_engine import IAnalysisEngine
from app.domain.interfaces.services.user_permissions import IUserPermissions


@dataclass
class AnalysisRequest:
    """분석 요청 DTO"""
    question: str
    user_id: str
    connection_id: Optional[str] = None
    file_data: Optional[bytes] = None
    options: Optional[Dict[str, Any]] = None


@dataclass
class AnalysisResponse:
    """분석 응답 DTO"""
    query_id: str
    question: str
    query_type: str
    status: str
    result: Optional[AnalysisResult] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None


class ExecuteAnalysisUseCase:
    """
    분석 실행 Use Case
    
    Clean Architecture: 이 클래스는 애플리케이션의 비즈니스 규칙을 구현합니다.
    - 도메인 엔티티와 값 객체를 사용
    - 인프라스트럭처에 의존하지 않음 (인터페이스를 통해 의존성 역전)
    - 단일 책임: 분석 실행 워크플로우만 담당
    """
    
    def __init__(
        self,
        query_repository: IQueryRepository,
        analysis_engine: IAnalysisEngine,
        user_permissions: IUserPermissions
    ):
        """
        의존성 주입을 통한 초기화
        
        Args:
            query_repository: 쿼리 저장소 인터페이스
            analysis_engine: 분석 엔진 인터페이스
            user_permissions: 사용자 권한 서비스 인터페이스
        """
        self._query_repository = query_repository
        self._analysis_engine = analysis_engine
        self._user_permissions = user_permissions
    
    async def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        분석 실행 메인 워크플로우
        
        Business Flow:
        1. 사용자 권한 검증
        2. 도메인 엔티티 생성
        3. 비즈니스 규칙 검증
        4. 분석 실행
        5. 결과 저장
        6. 응답 반환
        
        Args:
            request: 분석 요청
            
        Returns:
            AnalysisResponse: 분석 결과
            
        Raises:
            PermissionDeniedError: 권한 부족
            InvalidQueryError: 잘못된 쿼리
            AnalysisExecutionError: 분석 실행 실패
        """
        start_time = datetime.utcnow()
        
        try:
            # 1. 사용자 권한 검증 (비즈니스 규칙)
            if not await self._user_permissions.can_execute_analysis(request.user_id):
                raise PermissionDeniedError("사용자에게 분석 실행 권한이 없습니다")
            
            # 2. 도메인 엔티티 생성
            query = AnalysisQuery.create_new(
                id=str(uuid.uuid4()),
                question=request.question,
                user_id=request.user_id,
                connection_id=request.connection_id,
                created_at=start_time
            )
            
            # 3. 비즈니스 규칙 검증
            if not query.is_valid():
                raise InvalidQueryError("쿼리가 비즈니스 규칙을 만족하지 않습니다")
            
            # 4. 분석 실행 (도메인 서비스에 위임)
            analysis_result = await self._analysis_engine.execute_analysis(
                question=query.question,
                connection_id=query.connection_id,
                file_data=request.file_data,
                options=request.options or {}
            )
            
            # 5. 성공 상태로 업데이트
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            query.mark_completed(execution_time)
            
            # 6. 결과 저장
            await self._query_repository.save(query)
            
            return AnalysisResponse(
                query_id=query.id,
                question=query.question,
                query_type=query.query_type.value,
                status=query.status.value,
                result=analysis_result,
                execution_time_ms=execution_time
            )
            
        except (PermissionDeniedError, InvalidQueryError) as e:
            # 비즈니스 규칙 위반 - 사용자 오류
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # 실패한 쿼리도 기록 (감사 목적)
            if 'query' in locals():
                query.mark_failed(str(e), execution_time)
                await self._query_repository.save(query)
            
            return AnalysisResponse(
                query_id=query.id if 'query' in locals() else str(uuid.uuid4()),
                question=request.question,
                query_type="unknown",
                status="failed",
                error_message=str(e),
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            # 시스템 오류
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            if 'query' in locals():
                query.mark_failed(f"시스템 오류: {str(e)}", execution_time)
                await self._query_repository.save(query)
            
            raise AnalysisExecutionError(f"분석 실행 중 오류 발생: {str(e)}")


# 도메인 예외 클래스들
class PermissionDeniedError(Exception):
    """권한 부족 예외"""
    pass


class InvalidQueryError(Exception):
    """잘못된 쿼리 예외"""
    pass


class AnalysisExecutionError(Exception):
    """분석 실행 오류 예외"""
    pass
