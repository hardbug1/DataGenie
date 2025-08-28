"""
Database Connection Model

Clean Architecture: Infrastructure model for external database connections
"""

import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class DatabaseConnection(Base):
    """
    Database connection configuration model.
    
    Stores encrypted connection details for external databases.
    
    SOLID: Single responsibility - manages database connection metadata
    Security: Connection details should be encrypted before storage
    """
    
    __tablename__ = "database_connections"
    __allow_unmapped__ = True  # SQLAlchemy 2.x 호환성
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique connection identifier"
    )
    
    # Owner reference
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
        comment="User who owns this connection"
    )
    
    # Connection metadata
    name = Column(
        String(100), 
        nullable=False,
        comment="User-friendly connection name"
    )
    
    description = Column(
        Text,
        comment="Optional description of the connection"
    )
    
    database_type = Column(
        String(20), 
        nullable=False,
        comment="Database type (postgresql, mysql, sqlite, etc.)"
    )
    
    # Connection details (encrypted)
    encrypted_config = Column(
        Text, 
        nullable=False,
        comment="Encrypted connection configuration (JSON)"
    )
    
    # Status and metadata
    is_active = Column(
        Boolean, 
        nullable=False, 
        default=True,
        comment="Whether this connection is active"
    )
    
    last_tested_at = Column(
        DateTime(timezone=True),
        comment="When the connection was last tested"
    )
    
    last_test_success = Column(
        Boolean,
        comment="Whether the last connection test succeeded"
    )
    
    last_test_error = Column(
        Text,
        comment="Error message from last failed test"
    )
    
    # Schema information cache
    schema_cache = Column(
        Text,
        comment="Cached schema information (JSON)"
    )
    
    schema_cached_at = Column(
        DateTime(timezone=True),
        comment="When schema was last cached"
    )
    
    # Metadata
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="When the connection was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now(),
        comment="When the connection was last updated"
    )
    
    # Relationships
    user: "User" = relationship(
        "User",
        back_populates="database_connections"
    )
    
    def __repr__(self) -> str:
        return f"<DatabaseConnection(id={self.id}, name='{self.name}', type='{self.database_type}')>"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.database_type})"
    
    # Domain methods
    def is_connection_healthy(self) -> bool:
        """
        Check if the connection is considered healthy.
        
        Business rule: A connection is healthy if it was tested recently
        and the test succeeded.
        """
        if not self.last_tested_at or not self.last_test_success:
            return False
        
        # Consider connection stale if not tested in the last hour
        time_since_test = datetime.utcnow() - self.last_tested_at
        return time_since_test.total_seconds() < 3600
    
    def needs_schema_refresh(self) -> bool:
        """
        Check if schema cache needs to be refreshed.
        
        Business rule: Schema should be refreshed every 24 hours
        """
        if not self.schema_cached_at:
            return True
        
        time_since_cache = datetime.utcnow() - self.schema_cached_at
        return time_since_cache.total_seconds() > 86400  # 24 hours
    
    def update_test_result(self, success: bool, error: str = None) -> None:
        """Update the connection test result."""
        self.last_tested_at = datetime.utcnow()
        self.last_test_success = success
        self.last_test_error = error
    
    def update_schema_cache(self, schema_info: Dict[str, Any]) -> None:
        """Update the cached schema information."""
        self.schema_cache = json.dumps(schema_info, default=str)
        self.schema_cached_at = datetime.utcnow()
    
    def get_schema_cache(self) -> Optional[Dict[str, Any]]:
        """Get the cached schema information."""
        if not self.schema_cache:
            return None
        
        try:
            return json.loads(self.schema_cache)
        except json.JSONDecodeError:
            return None
    
    def get_connection_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the connection for API responses.
        
        Note: This excludes sensitive connection details.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "database_type": self.database_type,
            "is_active": self.is_active,
            "is_healthy": self.is_connection_healthy(),
            "last_tested_at": self.last_tested_at.isoformat() if self.last_tested_at else None,
            "last_test_success": self.last_test_success,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def create_new_connection(
        cls,
        user_id: uuid.UUID,
        name: str,
        database_type: str,
        encrypted_config: str,
        description: str = None
    ) -> "DatabaseConnection":
        """
        Factory method to create a new database connection.
        
        Args:
            user_id: ID of the user who owns this connection
            name: User-friendly name for the connection
            database_type: Type of database (postgresql, mysql, etc.)
            encrypted_config: Encrypted connection configuration
            description: Optional description
        
        Returns:
            New DatabaseConnection instance
        """
        return cls(
            user_id=user_id,
            name=name,
            database_type=database_type,
            encrypted_config=encrypted_config,
            description=description,
            is_active=True
        )
