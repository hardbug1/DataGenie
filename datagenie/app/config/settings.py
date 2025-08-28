"""
DataGenie Application Settings

Clean Architecture: Configuration belongs in Infrastructure layer
but is accessed by all layers through dependency injection.
"""

import os
import secrets
from typing import List, Optional, Any, Dict
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.
    
    SOLID: Single Responsibility - Only handles configuration
    TDD: Configuration should be testable and mockable
    """
    
    # Application Info
    app_name: str = Field(default="DataGenie", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=False, env="RELOAD")
    workers: int = Field(default=1, env="WORKERS")
    
    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="SECRET_KEY")
    jwt_secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    encryption_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="ENCRYPTION_KEY")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    openai_model_fallback: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL_FALLBACK")
    openai_max_tokens: int = Field(default=2000, env="OPENAI_MAX_TOKENS")
    openai_temperature: float = Field(default=0.0, env="OPENAI_TEMPERATURE")
    
    # LLM Engine Configuration
    use_llm_engine: bool = Field(default=False, env="USE_LLM_ENGINE")
    llm_cache_ttl: int = Field(default=3600, env="LLM_CACHE_TTL")
    llm_max_retries: int = Field(default=2, env="LLM_MAX_RETRIES")
    llm_timeout: int = Field(default=30, env="LLM_TIMEOUT")
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/datagenie",
        env="DATABASE_URL"
    )
    database_host: str = Field(default="localhost", env="DATABASE_HOST")
    database_port: int = Field(default=5432, env="DATABASE_PORT")
    database_name: str = Field(default="datagenie", env="DATABASE_NAME")
    database_user: str = Field(default="postgres", env="DATABASE_USER")
    database_password: str = Field(default="password", env="DATABASE_PASSWORD")
    database_pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    database_pool_overflow: int = Field(default=10, env="DATABASE_POOL_OVERFLOW")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_cache_ttl: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # File Upload Configuration
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    allowed_file_types: str = Field(
        default=".xlsx,.xls,.csv", 
        env="ALLOWED_FILE_TYPES"
    )
    
    # Security Settings
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        env="CORS_ORIGINS"
    )
    trusted_hosts: str = Field(
        default="localhost,127.0.0.1",
        env="TRUSTED_HOSTS"
    )
    rate_limit_per_minute: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    
    # External Database Configuration
    external_db_configs: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_api_key(cls, v):
        """Validate OpenAI API key format"""
        # OpenAI API 키는 선택사항 (Mock 모드에서는 불필요)
        if v is None or v == "":
            return None
        
        if v == "your-openai-api-key-here":
            return None  # 기본값인 경우 None으로 처리
        
        if not v.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        
        return v
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @field_validator("allowed_file_types")
    @classmethod
    def validate_file_types(cls, v):
        """Validate file extensions"""
        if isinstance(v, str):
            exts = [ext.strip() for ext in v.split(",")]
            for ext in exts:
                if not ext.startswith("."):
                    raise ValueError(f"File extension must start with '.': {ext}")
        return v
    
    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v):
        """Validate CORS origins"""
        return v
    
    @field_validator("trusted_hosts")
    @classmethod
    def validate_trusted_hosts(cls, v):
        """Validate trusted hosts"""
        return v
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes"""
        return self.max_file_size_mb * 1024 * 1024
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.debug or self.reload
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.is_development
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Get allowed file types as a list"""
        return [ext.strip() for ext in self.allowed_file_types.split(",")]
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def trusted_hosts_list(self) -> List[str]:
        """Get trusted hosts as a list"""
        return [host.strip() for host in self.trusted_hosts.split(",")]
    
    def get_database_url(self, async_driver: bool = True) -> str:
        """Generate database URL with appropriate driver"""
        driver = "postgresql+asyncpg" if async_driver else "postgresql"
        return f"{driver}://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    def get_redis_url(self) -> str:
        """Generate Redis URL"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Clean Architecture: This is a factory function that provides
    settings to the application. Uses LRU cache for performance.
    
    TDD: Can be easily mocked in tests by clearing the cache
    and patching environment variables.
    """
    return Settings()


# Export settings instance
settings = get_settings()
