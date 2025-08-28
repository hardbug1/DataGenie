"""
User Model

Clean Architecture: This is an infrastructure model that represents
users in the database. Domain logic should be kept separate.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, Boolean, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.config.database import Base


class User(Base):
    """
    User model representing system users.
    
    SOLID: Single responsibility - represents user data
    Clean Architecture: Infrastructure layer entity
    """
    
    __tablename__ = "users"
    __allow_unmapped__ = True  # SQLAlchemy 2.x 호환성
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # Authentication fields
    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        index=True
    )
    
    email: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(String(255))
    
    # Profile fields
    full_name: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    
    # Role and permissions
    role: Mapped[str] = mapped_column(String(20), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None
    )
    
    # Additional profile data (JSON field for flexibility)
    profile_data: Mapped[Optional[str]] = mapped_column(Text, default=None)
    
    # Relationships (using string-based forward references)
    database_connections: Mapped[List["DatabaseConnection"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    query_histories: Mapped[List["QueryHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    user_sessions: Mapped[List["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def __str__(self) -> str:
        return f"{self.full_name or self.username} ({self.email})"
    
    # Domain methods (business logic)
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"
    
    @property
    def can_access_admin_features(self) -> bool:
        """Check if user can access admin features."""
        return self.is_admin and self.is_active and self.is_verified
    
    def can_create_database_connection(self) -> bool:
        """
        Business rule: Check if user can create database connections.
        
        This is domain logic that could be moved to a domain service.
        """
        return self.is_active and self.is_verified
    
    def can_execute_query(self) -> bool:
        """
        Business rule: Check if user can execute queries.
        """
        return self.is_active and self.is_verified
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login_at = datetime.utcnow()
    
    @classmethod
    def create_new_user(
        cls,
        username: str,
        email: str,
        password_hash: str,
        full_name: str = None,
        role: str = "user"
    ) -> "User":
        """
        Factory method to create a new user.
        
        This encapsulates user creation logic and ensures
        all required fields are set correctly.
        """
        return cls(
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            role=role,
            is_active=True,
            is_verified=False  # Require email verification
        )
