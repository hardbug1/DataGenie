"""
Query History Model

Clean Architecture: Infrastructure model for storing query execution history
"""

import uuid
import json
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class QueryHistory(Base):
    """
    Query execution history model.
    
    Stores information about user queries, generated SQL/code,
    execution results, and analysis insights.
    
    SOLID: Single responsibility - manages query execution records
    """
    
    __tablename__ = "query_history"
    __allow_unmapped__ = True  # SQLAlchemy 2.x 호환성
    
    # Primary key
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique query execution identifier"
    )
    
    # User reference
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
        comment="User who executed this query"
    )
    
    # Database connection reference (optional for Excel analysis)
    connection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("database_connections.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Database connection used (null for Excel analysis)"
    )
    
    # Query information
    original_question = Column(
        Text, 
        nullable=False,
        comment="Original natural language question from user"
    )
    
    query_type = Column(
        String(20), 
        nullable=False,
        comment="Type of query (database, excel, general)"
    )
    
    generated_query = Column(
        Text,
        comment="Generated SQL query or Python code"
    )
    
    # Execution information
    execution_status = Column(
        String(20), 
        nullable=False,
        comment="Execution status (pending, running, completed, failed)"
    )
    
    started_at = Column(
        DateTime(timezone=True),
        comment="When query execution started"
    )
    
    completed_at = Column(
        DateTime(timezone=True),
        comment="When query execution completed"
    )
    
    execution_time_ms = Column(
        Integer,
        comment="Execution time in milliseconds"
    )
    
    # Results
    result_rows = Column(
        Integer,
        comment="Number of rows returned"
    )
    
    result_data = Column(
        Text,
        comment="Query results (JSON, limited size)"
    )
    
    # Error handling
    error_message = Column(
        Text,
        comment="Error message if execution failed"
    )
    
    error_type = Column(
        String(50),
        comment="Type of error (syntax, permission, timeout, etc.)"
    )
    
    # Analysis and insights
    analysis_insights = Column(
        Text,
        comment="AI-generated insights about the results (JSON)"
    )
    
    visualization_config = Column(
        Text,
        comment="Visualization configuration (JSON)"
    )
    
    # Quality metrics
    confidence_score = Column(
        Float,
        comment="AI confidence score for the generated query (0.0-1.0)"
    )
    
    user_feedback = Column(
        String(20),
        comment="User feedback (helpful, not_helpful, etc.)"
    )
    
    # Metadata
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(),
        comment="When the query was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now(),
        comment="When the query was last updated"
    )
    
    # Relationships
    user: "User" = relationship(
        "User",
        back_populates="query_histories"
    )
    
    connection = relationship(
        "DatabaseConnection",
        foreign_keys=[connection_id]
    )
    
    def __repr__(self) -> str:
        return f"<QueryHistory(id={self.id}, type='{self.query_type}', status='{self.execution_status}')>"
    
    def __str__(self) -> str:
        return f"Query: {self.original_question[:50]}..."
    
    # Domain methods
    @property
    def is_completed(self) -> bool:
        """Check if query execution is completed."""
        return self.execution_status in ["completed", "failed"]
    
    @property
    def is_successful(self) -> bool:
        """Check if query execution was successful."""
        return self.execution_status == "completed" and self.error_message is None
    
    @property
    def execution_time_seconds(self) -> Optional[float]:
        """Get execution time in seconds."""
        if self.execution_time_ms is None:
            return None
        return self.execution_time_ms / 1000.0
    
    def start_execution(self) -> None:
        """Mark query execution as started."""
        self.execution_status = "running"
        self.started_at = datetime.utcnow()
    
    def complete_execution(
        self, 
        result_data: Optional[str] = None,
        result_rows: Optional[int] = None,
        insights: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark query execution as completed successfully."""
        self.execution_status = "completed"
        self.completed_at = datetime.utcnow()
        
        if self.started_at:
            execution_time = self.completed_at - self.started_at
            self.execution_time_ms = int(execution_time.total_seconds() * 1000)
        
        if result_data is not None:
            self.result_data = result_data
        
        if result_rows is not None:
            self.result_rows = result_rows
            
        if insights is not None:
            self.analysis_insights = json.dumps(insights, default=str)
    
    def fail_execution(self, error_message: str, error_type: str = None) -> None:
        """Mark query execution as failed."""
        self.execution_status = "failed"
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
        self.error_type = error_type
        
        if self.started_at:
            execution_time = self.completed_at - self.started_at
            self.execution_time_ms = int(execution_time.total_seconds() * 1000)
    
    def get_insights(self) -> Optional[Dict[str, Any]]:
        """Get parsed analysis insights."""
        if not self.analysis_insights:
            return None
        
        try:
            return json.loads(self.analysis_insights)
        except json.JSONDecodeError:
            return None
    
    def get_visualization_config(self) -> Optional[Dict[str, Any]]:
        """Get parsed visualization configuration."""
        if not self.visualization_config:
            return None
        
        try:
            return json.loads(self.visualization_config)
        except json.JSONDecodeError:
            return None
    
    def get_result_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the query execution for API responses.
        """
        return {
            "id": str(self.id),
            "original_question": self.original_question,
            "query_type": self.query_type,
            "execution_status": self.execution_status,
            "is_successful": self.is_successful,
            "result_rows": self.result_rows,
            "execution_time_seconds": self.execution_time_seconds,
            "confidence_score": self.confidence_score,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "error_type": self.error_type
        }
    
    @classmethod
    def create_new_query(
        cls,
        user_id: uuid.UUID,
        original_question: str,
        query_type: str,
        connection_id: Optional[uuid.UUID] = None,
        generated_query: Optional[str] = None,
        confidence_score: Optional[float] = None
    ) -> "QueryHistory":
        """
        Factory method to create a new query history entry.
        
        Args:
            user_id: ID of the user executing the query
            original_question: The natural language question
            query_type: Type of query (database, excel, general)
            connection_id: Database connection ID (if applicable)
            generated_query: Generated SQL or Python code
            confidence_score: AI confidence score
        
        Returns:
            New QueryHistory instance
        """
        return cls(
            user_id=user_id,
            connection_id=connection_id,
            original_question=original_question,
            query_type=query_type,
            generated_query=generated_query,
            execution_status="pending",
            confidence_score=confidence_score
        )
