"""
Logging Configuration for DataGenie

Clean Architecture: Logging is a cross-cutting concern
that should be properly configured at application startup.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any

import structlog
from structlog.types import Processor
from rich.logging import RichHandler
from rich.console import Console

from app.config.settings import get_settings


def setup_logging() -> None:
    """
    Setup structured logging for the application.
    
    SOLID: Single responsibility - only configures logging
    Clean Architecture: Infrastructure concern
    """
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog processors
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    
    # Add different processors based on environment
    if settings.is_development:
        # Development: Pretty console output
        processors.extend([
            structlog.dev.set_exc_info,
            structlog.dev.ConsoleRenderer(colors=True)
        ])
    else:
        # Production: JSON output
        processors.extend([
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ])
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    _configure_stdlib_logging(settings)
    
    # Log configuration
    logger = structlog.get_logger(__name__)
    logger.info(
        "Logging configured",
        log_level=settings.log_level,
        log_format=settings.log_format,
        log_file=settings.log_file,
        development_mode=settings.is_development
    )


def _configure_stdlib_logging(settings) -> None:
    """Configure Python standard library logging."""
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    if settings.is_development:
        # Rich console handler for development
        console = Console(force_terminal=True)
        console_handler = RichHandler(
            console=console,
            show_time=True,
            show_level=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=True
        )
        console_handler.setLevel(getattr(logging, settings.log_level))
        root_logger.addHandler(console_handler)
    else:
        # Simple console handler for production
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.log_level))
        
        if settings.log_format == "json":
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s"}'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    try:
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setLevel(getattr(logging, settings.log_level))
        
        if settings.log_format == "json":
            file_formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s", '
                '"module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
            )
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
    except Exception as e:
        # If file logging fails, log to console
        root_logger.error(f"Failed to setup file logging: {e}")
    
    # Configure specific loggers
    _configure_third_party_loggers()


def _configure_third_party_loggers() -> None:
    """Configure logging levels for third-party libraries."""
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    # Redis logging
    logging.getLogger("redis").setLevel(logging.WARNING)
    logging.getLogger("aioredis").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.
    
    This is the recommended way to get loggers in the application.
    
    Args:
        name: Logger name, typically __name__
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LoggingMiddleware:
    """
    Logging middleware for FastAPI.
    
    Logs request/response information for debugging and monitoring.
    """
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger(__name__)
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Log request
            self.logger.info(
                "HTTP request started",
                method=scope["method"],
                path=scope["path"],
                query_string=scope.get("query_string", b"").decode(),
                client=scope.get("client")
            )
        
        await self.app(scope, receive, send)


# Context managers for structured logging
class LogContext:
    """Context manager for adding structured logging context."""
    
    def __init__(self, **context):
        self.context = context
        self.token = None
    
    def __enter__(self):
        self.token = structlog.contextvars.bind_contextvars(**self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token:
            structlog.contextvars.unbind_contextvars(*self.context.keys())


def log_function_call(func_name: str, **kwargs):
    """Decorator/context for logging function calls."""
    return LogContext(function=func_name, **kwargs)
