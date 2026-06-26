"""Pydantic models for Onspring list item API requests and responses."""

import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ListItemRequest(BaseModel):
    """Request payload for adding or updating a list item."""

    model_config = ConfigDict(populate_by_name=True)

    list_id: int = Field(alias="listId")
    name: str
    id: Optional[uuid.UUID] = None
    numeric_value: Optional[int] = Field(default=None, alias="numericValue")
    color: Optional[str] = None


class AddOrUpdateListItemResponse(BaseModel):
    """Response containing the ID of an added or updated list item."""

    id: uuid.UUID
