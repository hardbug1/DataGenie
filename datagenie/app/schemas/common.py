"""
Common Pydantic Schemas

Clean Architecture: These are interface layer components
that define the structure of API requests and responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

# Generic type for paginated responses
T = TypeVar('T')


class BaseResponse(BaseModel):
    """
    Base response schema for all API responses.
    
    SOLID: Open-Closed Principle - all responses extend this base
    """
    
    success: bool = Field(
        ...,
        description="Whether the request was successful"
    )
    
    message: str = Field(
        default="Request processed successfully",
        description="Human-readable message"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    request_id: Optional[str] = Field(
        default=None,
        description="Unique request identifier for tracing"
    )


class SuccessResponse(BaseResponse):
    """
    Standard success response schema.
    
    Used for operations that don't return specific data.
    """
    
    success: bool = Field(default=True)
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional response data"
    )


class ErrorResponse(BaseResponse):
    """
    Standard error response schema.
    
    Provides consistent error reporting across the API.
    """
    
    success: bool = Field(default=False)
    error: Dict[str, Any] = Field(
        ...,
        description="Error details"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Validation error",
                "timestamp": "2023-12-01T10:00:00Z",
                "request_id": "req_123456",
                "error": {
                    "type": "ValidationError",
                    "code": "INVALID_INPUT",
                    "details": {
                        "field": "email",
                        "issue": "Invalid email format"
                    }
                }
            }
        }


class PaginatedResponse(BaseResponse, Generic[T]):
    """
    Paginated response schema for list endpoints.
    
    Generic type allows type-safe pagination for any data type.
    """
    
    success: bool = Field(default=True)
    data: List[T] = Field(
        ...,
        description="List of items for current page"
    )
    
    pagination: Dict[str, Any] = Field(
        ...,
        description="Pagination metadata"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Data retrieved successfully",
                "timestamp": "2023-12-01T10:00:00Z",
                "data": [
                    {"id": "1", "name": "Item 1"},
                    {"id": "2", "name": "Item 2"}
                ],
                "pagination": {
                    "current_page": 1,
                    "total_pages": 5,
                    "total_items": 100,
                    "items_per_page": 20,
                    "has_next": True,
                    "has_previous": False
                }
            }
        }


class PaginationRequest(BaseModel):
    """
    Standard pagination request parameters.
    
    Can be used as a dependency in FastAPI endpoints.
    """
    
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (1-based)"
    )
    
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page (max 100)"
    )
    
    sort_by: Optional[str] = Field(
        default=None,
        description="Field to sort by"
    )
    
    sort_order: Optional[str] = Field(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort order (asc or desc)"
    )
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.limit


class HealthResponse(BaseModel):
    """
    Health check response schema.
    
    Used by monitoring systems to check service health.
    """
    
    status: str = Field(
        ...,
        description="Overall health status"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Health check timestamp"
    )
    
    service: str = Field(
        default="DataGenie",
        description="Service name"
    )
    
    version: str = Field(
        default="0.1.0",
        description="Service version"
    )
    
    checks: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Detailed health check results"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2023-12-01T10:00:00Z",
                "service": "DataGenie",
                "version": "0.1.0",
                "checks": {
                    "database": "healthy",
                    "redis": "healthy",
                    "openai": "healthy"
                }
            }
        }


class ValidationErrorDetail(BaseModel):
    """
    Validation error detail schema.
    
    Provides structured validation error information.
    """
    
    field: str = Field(
        ...,
        description="Field that failed validation"
    )
    
    message: str = Field(
        ...,
        description="Validation error message"
    )
    
    type: str = Field(
        ...,
        description="Type of validation error"
    )
    
    input_value: Any = Field(
        default=None,
        description="Value that failed validation"
    )


class BulkOperationRequest(BaseModel):
    """
    Base schema for bulk operations.
    
    Supports batch processing of multiple items.
    """
    
    items: List[Dict[str, Any]] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of items to process (max 100)"
    )
    
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional options for bulk operation"
    )


class BulkOperationResponse(BaseResponse):
    """
    Response schema for bulk operations.
    
    Provides detailed results for each item in the batch.
    """
    
    success: bool = Field(default=True)
    results: List[Dict[str, Any]] = Field(
        ...,
        description="Results for each item in the batch"
    )
    
    summary: Dict[str, Any] = Field(
        ...,
        description="Summary of bulk operation results"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Bulk operation completed",
                "timestamp": "2023-12-01T10:00:00Z",
                "results": [
                    {"id": "1", "success": True, "message": "Created successfully"},
                    {"id": "2", "success": False, "error": "Validation failed"}
                ],
                "summary": {
                    "total": 2,
                    "successful": 1,
                    "failed": 1,
                    "processing_time_ms": 150
                }
            }
        }


class FileUploadResponse(BaseResponse):
    """
    File upload response schema.
    
    Used for Excel file uploads and other file operations.
    """
    
    success: bool = Field(default=True)
    file_info: Dict[str, Any] = Field(
        ...,
        description="Information about the uploaded file"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "File uploaded successfully",
                "timestamp": "2023-12-01T10:00:00Z",
                "file_info": {
                    "file_id": "file_123456",
                    "filename": "sales_data.xlsx",
                    "size_bytes": 1024000,
                    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "sheets": ["Sales", "Products"],
                    "rows": 1500,
                    "columns": 10
                }
            }
        }
