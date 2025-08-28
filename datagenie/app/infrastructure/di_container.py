"""
Dependency Injection Container

Clean Architecture: Composition Root
모든 의존성을 연결하는 중앙 집중식 컨테이너
"""

from functools import lru_cache
import structlog

from app.use_cases.analysis.execute_analysis_use_case import ExecuteAnalysisUseCase
from app.use_cases.auth.authenticate_user_use_case import AuthenticateUserUseCase

# 실제 구현체들
from app.infrastructure.adapters.repositories.sqlalchemy_query_repository import SQLAlchemyQueryRepository
from app.infrastructure.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.adapters.services.llm_analysis_engine import LLMAnalysisEngine
from app.infrastructure.adapters.services.database_user_permissions import DatabaseUserPermissions

# Mock 구현체들 (테스트/개발용)
from app.infrastructure.adapters.repositories.mock_query_repository import MockQueryRepository
from app.infrastructure.adapters.repositories.mock_user_repository import MockUserRepository
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
            
            # 환경에 따라 실제 구현체 또는 Mock 사용 결정
            use_real_implementations = self._should_use_real_implementations()
            
            if use_real_implementations:
                # 실제 구현체들 사용
                self._query_repository = SQLAlchemyQueryRepository()
                self._user_repository = SQLAlchemyUserRepository()
                self._analysis_engine = LLMAnalysisEngine()
                self._user_permissions = DatabaseUserPermissions()
                logger.info("실제 구현체들 사용 (Production Mode)")
            else:
                # Mock 구현체들 사용 (개발/테스트)
                self._query_repository = MockQueryRepository()
                self._user_repository = MockUserRepository()
                self._analysis_engine = MockAnalysisEngine()
                self._user_permissions = MockUserPermissions()
                logger.info("Mock 구현체들 사용 (Development/Test Mode)")
            
            # Use Cases (Application Layer)
            self._execute_analysis_use_case = ExecuteAnalysisUseCase(
                query_repository=self._query_repository,
                analysis_engine=self._analysis_engine,
                user_permissions=self._user_permissions
            )
            
            self._authenticate_user_use_case = AuthenticateUserUseCase(
                user_repository=self._user_repository
            )
            
            logger.info(
                "DI Container 서비스 초기화 완료",
                real_implementations_enabled=use_real_implementations
            )
            
        except Exception as e:
            logger.error("DI Container 초기화 실패", error=str(e))
            raise
    
    def _should_use_real_implementations(self) -> bool:
        """실제 구현체 사용 여부 결정"""
        import os
        
        # 환경 변수로 제어
        use_real = os.getenv("USE_REAL_IMPLEMENTATIONS", "false").lower() == "true"
        
        # OpenAI API 키가 있는지 확인 (LLM 엔진 사용을 위해)
        api_key = os.getenv("OPENAI_API_KEY")
        has_api_key = bool(api_key and api_key != "your-openai-api-key-here")
        
        # 데이터베이스 URL 확인
        has_database = bool(os.getenv("DATABASE_URL"))
        
        # 실제 구현체 사용 조건:
        # 1. USE_REAL_IMPLEMENTATIONS=true
        # 2. 데이터베이스 URL 설정됨
        # 3. LLM 사용시에만 OpenAI API 키 필요
        can_use_real = use_real and has_database
        
        logger.debug(
            "실제 구현체 사용 여부 확인",
            use_real=use_real,
            has_api_key=has_api_key,
            has_database=has_database,
            can_use_real=can_use_real
        )
        
        return can_use_real
    
    def get_execute_analysis_use_case(self) -> ExecuteAnalysisUseCase:
        """분석 실행 Use Case 반환"""
        self._ensure_initialized()
        return self._execute_analysis_use_case
    
    def get_authenticate_user_use_case(self) -> AuthenticateUserUseCase:
        """사용자 인증 Use Case 반환"""
        self._ensure_initialized()
        return self._authenticate_user_use_case
    
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
