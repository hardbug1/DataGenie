"""
Database Models for DataGenie

Clean Architecture: Models represent entities and are part of the infrastructure layer
when they contain database-specific details (SQLAlchemy), but can also represent
domain entities when they contain business logic.
"""

from app.models.user import User
from app.models.database_connection import DatabaseConnection
from app.models.query_history import QueryHistory
from app.models.user_session import UserSession

__all__ = [
    "User",
    "DatabaseConnection", 
    "QueryHistory",
    "UserSession"
]
