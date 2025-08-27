"""
Logging Configuration

Clean Architecture: Infrastructure 설정
구조화된 로깅 시스템 설정
"""

import sys
import logging
import structlog
from typing import Any

from app.config.settings import get_settings

settings = get_settings()


def setup_logging() -> None:
    """
    구조화된 로깅 시스템 설정
    
    - JSON 형태의 구조화된 로그
    - 개발/운영 환경별 다른 설정
    - 성능 최적화된 로깅
    """
    
    # 기본 로깅 설정
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )
    
    # structlog 프로세서 설정
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # 환경별 다른 렌더러 사용
    if settings.debug:
        # 개발 환경: 읽기 쉬운 콘솔 출력
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        # 운영 환경: JSON 형태 출력
        processors.append(structlog.processors.JSONRenderer())
    
    # structlog 설정
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # 외부 라이브러리 로그 레벨 조정
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    if not settings.debug:
        # 운영 환경에서는 더 높은 레벨로 설정
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> Any:
    """
    구조화된 로거 인스턴스 반환
    
    Args:
        name: 로거 이름
        
    Returns:
        structlog 로거 인스턴스
    """
    return structlog.get_logger(name)