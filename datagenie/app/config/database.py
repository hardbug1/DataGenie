"""
Database Configuration and Connection Management

Clean Architecture: Infrastructure layer responsible for database setup
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import structlog

from app.config.settings import get_settings

logger = structlog.get_logger(__name__)

# SQLAlchemy Base
Base = declarative_base()

# Global variables for engine and session maker
_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def create_database_engine() -> AsyncEngine:
    """
    Create async database engine.
    
    Clean Architecture: This is an infrastructure detail
    that creates the database connection.
    
    SOLID: Single responsibility - only creates engine
    """
    settings = get_settings()
    
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,  # Log SQL queries in debug mode
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_pool_overflow,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=3600,   # Recycle connections every hour
        # Use NullPool for testing to avoid connection issues
        poolclass=NullPool if settings.debug else None,
    )
    
    logger.info(
        "Database engine created",
        database_url=settings.database_url.split('@')[1] if '@' in settings.database_url else settings.database_url,
        pool_size=settings.database_pool_size,
        debug=settings.debug
    )
    
    return engine


def get_database_engine() -> AsyncEngine:
    """
    Get or create database engine.
    
    Lazy initialization pattern for better performance.
    """
    global _engine
    if _engine is None:
        _engine = create_database_engine()
    return _engine


def create_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Create async session maker.
    
    Clean Architecture: Session maker is part of infrastructure
    that provides database sessions to use cases.
    """
    engine = get_database_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Allow access to objects after commit
        autoflush=True,         # Automatically flush before queries
        autocommit=False        # Manual transaction control
    )


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """Get or create session maker."""
    global _async_session_maker
    if _async_session_maker is None:
        _async_session_maker = create_session_maker()
    return _async_session_maker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session for repositories.
    
    This is used by repository implementations to get
    database sessions for data operations.
    """
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            logger.debug("Async database session created")
            yield session
        except Exception as e:
            logger.error("Async database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug("Async database session closed")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    
    This is used with FastAPI's Depends() to inject
    database sessions into API endpoints.
    
    Clean Architecture: This provides the interface
    that use cases need to access the database.
    """
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            logger.debug("Database session created")
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug("Database session closed")


async def init_database() -> None:
    """
    Initialize database.
    
    This creates all tables defined in models.
    In production, this should be handled by Alembic migrations.
    """
    engine = get_database_engine()
    
    try:
        async with engine.begin() as conn:
            logger.info("Creating database tables")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise


async def close_database() -> None:
    """
    Close database connections.
    
    Should be called during application shutdown.
    """
    global _engine
    if _engine:
        logger.info("Closing database connections")
        await _engine.dispose()
        _engine = None
        logger.info("Database connections closed")


# Connection health check
async def check_database_health() -> bool:
    """
    Check database connection health.
    
    Returns True if database is accessible, False otherwise.
    """
    try:
        engine = get_database_engine()
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.debug("Database health check passed")
        return True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False
