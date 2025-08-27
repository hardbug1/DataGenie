"""
Dependency Injection Container

Clean Architecture: Composition Root
모든 의존성을 연결하는 중앙 집중식 컨테이너
"""

from functools import lru_cache
import structlog

from app.use_cases.analysis.execute_analysis_use_case import ExecuteAnalysisUseCase
from app.infrastructure.adapters.repositories.mock_query_repository import MockQueryRepository
from app.infrastructure.adapters.services.mock_analysis_engine import MockAnalysisEngine
from app.infrastructure.adapters.services.mock_user_permissions import MockUserPermissions

logger = structlog.get_logger(__name__)


class DIContainer:
    """
    의존성 주입 컨테이너
    
    Clean Architecture: Composition Root 패턴
    - 모든 의존성을 한 곳에서 관리
    - 인터페이스와 구현체를 연결
    - 싱글톤 패턴으로 인스턴스 관리
    """
    
    def __init__(self):
        """컨테이너 초기화"""
        self._services = {}
        self._initialized = False
        logger.info("DI Container 초기화")
    
    def _ensure_initialized(self):
        """지연 초기화"""
        if not self._initialized:
            self._initialize_services()
            self._initialized = True
    
    def _initialize_services(self):
        """서비스 초기화"""
        try:
            # Infrastructure Layer (가장 바깥쪽)
            # TODO: 실제 구현체로 교체 예정
            
            # Repositories
            self._query_repository = MockQueryRepository()
            
            # External Services
            self._analysis_engine = MockAnalysisEngine()
            self._user_permissions = MockUserPermissions()
            
            # Use Cases (Application Layer)
            self._execute_analysis_use_case = ExecuteAnalysisUseCase(
                query_repository=self._query_repository,
                analysis_engine=self._analysis_engine,
                user_permissions=self._user_permissions
            )
            
            logger.info("DI Container 서비스 초기화 완료")
            
        except Exception as e:
            logger.error("DI Container 초기화 실패", error=str(e))
            raise
    
    def get_execute_analysis_use_case(self) -> ExecuteAnalysisUseCase:
        """분석 실행 Use Case 반환"""
        self._ensure_initialized()
        return self._execute_analysis_use_case
    
    # 추가 서비스 getter 메서드들 (향후 구현)
    
    def get_query_repository(self):
        """쿼리 저장소 반환"""
        self._ensure_initialized()
        return self._query_repository
    
    def get_analysis_engine(self):
        """분석 엔진 반환"""
        self._ensure_initialized()
        return self._analysis_engine
    
    def get_user_permissions(self):
        """사용자 권한 서비스 반환"""
        self._ensure_initialized()
        return self._user_permissions


# 전역 컨테이너 인스턴스
_container: DIContainer = None


@lru_cache()
def get_di_container() -> DIContainer:
    """
    DI 컨테이너 싱글톤 인스턴스 반환
    
    Returns:
        DIContainer: 의존성 주입 컨테이너
    """
    global _container
    if _container is None:
        _container = DIContainer()
    return _container


def reset_di_container():
    """
    DI 컨테이너 초기화 (테스트용)
    """
    global _container
    _container = None
    get_di_container.cache_clear()
