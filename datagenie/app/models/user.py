"""
User Model

Clean Architecture: This is an infrastructure model that represents
users in the database. Domain logic should be kept separate.
"""

import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.database_connection import DatabaseConnection
    from app.models.query_history import QueryHistory
    from app.models.user_session import UserSession


class User(Base):
    """
    User model representing system users.
    
    SOLID: Single responsibility - represents user data
    Clean Architecture: Infrastructure layer entity
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique user identifier"
    )
    
    # Authentication fields
    username = Column(
        String(50), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="Unique username for login"
    )
    
    email = Column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="User email address"
    )
    
    password_hash = Column(
        String(255), 
        nullable=False,
        comment="Hashed password (bcrypt)"
    )
    
    # Profile fields
    full_name = Column(
        String(100),
        comment="User's full name"
    )
    
    # Role and permissions
    role = Column(
        String(20), 
        nullable=False, 
        default="user",
        comment="User role (admin, user, etc.)"
    )
    
    is_active = Column(
        Boolean, 
        nullable=False, 
        default=True,
        comment="Whether the user account is active"
    )
    
    is_verified = Column(
        Boolean, 
        nullable=False, 
        default=False,
        comment="Whether the user email is verified"
    )
    
    # Metadata
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="When the user was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now(),
        comment="When the user was last updated"
    )
    
    last_login_at = Column(
        DateTime(timezone=True),
        comment="When the user last logged in"
    )
    
    # Additional profile data (JSON field for flexibility)
    profile_data = Column(
        Text,
        comment="Additional profile data as JSON"
    )
    
    # Relationships
    database_connections: List["DatabaseConnection"] = relationship(
        "DatabaseConnection",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    query_histories: List["QueryHistory"] = relationship(
        "QueryHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    user_sessions: List["UserSession"] = relationship(
        "UserSession",
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
