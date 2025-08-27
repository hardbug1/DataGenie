"""
Pydantic Schemas for DataGenie API

Clean Architecture: Schemas represent the interface layer
and handle serialization/deserialization for API requests/responses.
"""

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    UserProfile
)
from app.schemas.auth import (
    TokenResponse,
    TokenData,
    LoginResponse,
    RefreshTokenRequest
)
from app.schemas.database_connection import (
    DatabaseConnectionCreate,
    DatabaseConnectionResponse,
    DatabaseConnectionUpdate,
    DatabaseConnectionTest
)
from app.schemas.query import (
    QueryRequest,
    QueryResponse,
    QueryHistory,
    QueryExecutionStatus
)
from app.schemas.common import (
    SuccessResponse,
    ErrorResponse,
    PaginatedResponse,
    HealthResponse
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse", 
    "UserUpdate",
    "UserLogin",
    "UserProfile",
    
    # Auth schemas
    "TokenResponse",
    "TokenData",
    "LoginResponse",
    "RefreshTokenRequest",
    
    # Database connection schemas
    "DatabaseConnectionCreate",
    "DatabaseConnectionResponse",
    "DatabaseConnectionUpdate", 
    "DatabaseConnectionTest",
    
    # Query schemas
    "QueryRequest",
    "QueryResponse",
    "QueryHistory",
    "QueryExecutionStatus",
    
    # Common schemas
    "SuccessResponse",
    "ErrorResponse",
    "PaginatedResponse",
    "HealthResponse"
]
