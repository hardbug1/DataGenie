"""
User Session Model

Clean Architecture: Infrastructure model for managing user sessions
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class UserSession(Base):
    """
    User session model for tracking active user sessions.
    
    This model helps with:
    - Session management
    - Security (detecting multiple sessions)
    - Analytics (user activity tracking)
    
    SOLID: Single responsibility - manages user session data
    """
    
    __tablename__ = "user_sessions"
    __allow_unmapped__ = True  # SQLAlchemy 2.x 호환성
    
    # Primary key
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique session identifier"
    )
    
    # User reference
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
        comment="User who owns this session"
    )
    
    # Session identification
    session_token = Column(
        String(255), 
        nullable=False, 
        unique=True,
        index=True,
        comment="Unique session token (JWT or similar)"
    )
    
    refresh_token = Column(
        String(255),
        nullable=True,
        unique=True,
        comment="Refresh token for extending session"
    )
    
    # Session metadata
    device_info = Column(
        Text,
        comment="Device information (User-Agent, etc.)"
    )
    
    ip_address = Column(
        String(45),  # IPv6 support
        comment="IP address of the client"
    )
    
    location = Column(
        String(100),
        comment="Geographic location (city, country)"
    )
    
    # Session timing
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="When the session was created"
    )
    
    expires_at = Column(
        DateTime(timezone=True), 
        nullable=False,
        comment="When the session expires"
    )
    
    last_activity_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="When the session was last used"
    )
    
    # Session status
    is_active = Column(
        Boolean, 
        nullable=False, 
        default=True,
        comment="Whether the session is active"
    )
    
    revoked_at = Column(
        DateTime(timezone=True),
        comment="When the session was revoked (logout)"
    )
    
    revoked_reason = Column(
        String(50),
        comment="Reason for revocation (logout, security, expired)"
    )
    
    # Relationships
    user: "User" = relationship(
        "User",
        back_populates="user_sessions"
    )
    
    def __repr__(self) -> str:
        return f"<UserSession(id={self.id}, user_id={self.user_id}, active={self.is_active})>"
    
    def __str__(self) -> str:
        return f"Session for {self.user_id} ({'active' if self.is_active else 'inactive'})"
    
    # Domain methods
    @property
    def is_expired(self) -> bool:
        """Check if the session has expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if the session is valid (active and not expired)."""
        return self.is_active and not self.is_expired and not self.revoked_at
    
    @property
    def time_until_expiry(self) -> Optional[timedelta]:
        """Get time until session expires."""
        if self.is_expired:
            return None
        return self.expires_at - datetime.utcnow()
    
    @property
    def age(self) -> timedelta:
        """Get session age."""
        return datetime.utcnow() - self.created_at
    
    @property
    def idle_time(self) -> timedelta:
        """Get time since last activity."""
        return datetime.utcnow() - self.last_activity_at
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity_at = datetime.utcnow()
    
    def extend_session(self, hours: int = 24) -> None:
        """
        Extend session expiration time.
        
        Args:
            hours: Number of hours to extend the session
        """
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        self.update_activity()
    
    def revoke_session(self, reason: str = "logout") -> None:
        """
        Revoke the session (logout).
        
        Args:
            reason: Reason for revocation
        """
        self.is_active = False
        self.revoked_at = datetime.utcnow()
        self.revoked_reason = reason
    
    def is_suspicious_activity(self) -> bool:
        """
        Check for suspicious session activity.
        
        Business logic for detecting potential security issues.
        """
        # Session is very old
        if self.age.total_seconds() > 30 * 24 * 3600:  # 30 days
            return True
        
        # Session has been idle for too long
        if self.idle_time.total_seconds() > 7 * 24 * 3600:  # 7 days
            return True
        
        return False
    
    def get_session_summary(self) -> dict:
        """
        Get session summary for API responses.
        
        Note: Excludes sensitive tokens.
        """
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "last_activity_at": self.last_activity_at.isoformat(),
            "is_active": self.is_active,
            "is_expired": self.is_expired,
            "is_valid": self.is_valid,
            "device_info": self.device_info,
            "ip_address": self.ip_address,
            "location": self.location,
            "age_hours": self.age.total_seconds() / 3600,
            "idle_hours": self.idle_time.total_seconds() / 3600,
            "time_until_expiry_hours": (
                self.time_until_expiry.total_seconds() / 3600
                if self.time_until_expiry else None
            )
        }
    
    @classmethod
    def create_new_session(
        cls,
        user_id: uuid.UUID,
        session_token: str,
        device_info: str = None,
        ip_address: str = None,
        location: str = None,
        expires_in_hours: int = 24
    ) -> "UserSession":
        """
        Factory method to create a new user session.
        
        Args:
            user_id: ID of the user
            session_token: Unique session token
            device_info: Device information
            ip_address: Client IP address
            location: Geographic location
            expires_in_hours: Session duration in hours
        
        Returns:
            New UserSession instance
        """
        return cls(
            user_id=user_id,
            session_token=session_token,
            device_info=device_info,
            ip_address=ip_address,
            location=location,
            expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
            is_active=True
        )
