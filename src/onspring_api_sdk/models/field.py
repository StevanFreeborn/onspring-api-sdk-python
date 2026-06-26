"""Pydantic models for Onspring field API responses."""

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ListValue(BaseModel):
    """A selectable value within a list field definition."""

    model_config = ConfigDict(populate_by_name=True)

    id: uuid.UUID
    name: str
    sort_order: int = Field(alias="sortOrder")
    numeric_value: Optional[int] = Field(default=None, alias="numericValue")
    color: Optional[str] = None


class OnspringField(BaseModel):
    """Represents an Onspring field definition."""

    model_config = ConfigDict(populate_by_name=True)

    id: int
    app_id: int = Field(alias="appId")
    name: str
    type: str
    status: str
    is_required: bool = Field(alias="isRequired")
    is_unique: bool = Field(alias="isUnique")
    list_id: Optional[int] = Field(default=None, alias="listId")
    values: Optional[list[ListValue]] = None
    multiplicity: Optional[str] = None
    output_type: Optional[str] = Field(default=None, alias="outputType")


class GetFieldByIdResponse(BaseModel):
    """Response containing a single field."""

    field: OnspringField


class GetFieldsByIdsResponse(BaseModel):
    """Response containing fields for requested IDs."""

    model_config = ConfigDict(populate_by_name=True)

    count: int
    fields: list[OnspringField] = Field(alias="items")


class GetFieldsByAppIdResponse(BaseModel):
    """Paginated response containing fields for an app."""

    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_records: int = Field(alias="totalRecords")
    fields: list[OnspringField] = Field(alias="items")
