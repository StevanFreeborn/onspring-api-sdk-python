"""Shared Pydantic models for paging and generic API responses."""

from typing import Generic, Optional, TypeVar

from httpx import Response
from pydantic import BaseModel, ConfigDict, Field, model_validator

from onspring_api_sdk.errors import (
    OnspringAuthenticationError,
    OnspringError,
    OnspringNotFoundError,
    OnspringRateLimitError,
)

T = TypeVar("T")


class PagingRequest(BaseModel):
    """Paging parameters for paginated API requests."""

    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(alias="pageNumber", default=1)
    page_size: int = Field(alias="pageSize", default=50)


class ApiResponse(BaseModel, Generic[T]):
    """Generic wrapper for all API responses with status and error handling."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    status_code: int
    is_successful: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    raw_response: Optional[Response] = None

    @model_validator(mode="before")
    @classmethod
    def set_is_successful(cls, data):
        """Automatically infer is_successful from status_code if not provided."""
        if isinstance(data, dict) and "is_successful" not in data and "status_code" in data:
            data["is_successful"] = int(data["status_code"]) < 400
        return data

    def raise_for_status(self):
        """Raise the appropriate exception if the request was not successful."""
        if not self.is_successful:
            if self.status_code in (401, 403):
                raise OnspringAuthenticationError(self.message or "Authentication failed")
            if self.status_code == 404:
                raise OnspringNotFoundError(self.message or "Resource not found")
            if self.status_code == 429:
                raise OnspringRateLimitError(self.message or "Rate limit exceeded")
            raise OnspringError(self.message or f"Request failed with status {self.status_code}")
