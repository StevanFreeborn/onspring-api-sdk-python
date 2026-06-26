"""Pydantic models for Onspring file API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class File(BaseModel):
    """Represents a file with its metadata and binary content."""

    model_config = ConfigDict(populate_by_name=True)

    name: str
    content_type: str = Field(alias="contentType")
    content_length: int = Field(alias="contentLength")
    content: bytes


class FileInfo(BaseModel):
    """Metadata about a file stored in Onspring."""

    model_config = ConfigDict(populate_by_name=True)

    type: str
    content_type: str = Field(alias="contentType")
    name: str
    created_date: Optional[datetime] = Field(default=None, alias="createdDate")
    modified_date: Optional[datetime] = Field(default=None, alias="modifiedDate")
    owner: str
    file_href: str = Field(alias="fileHref")


class GetFileInfoByIdResponse(BaseModel):
    """Response containing file metadata."""

    model_config = ConfigDict(populate_by_name=True)

    file_info: FileInfo = Field(alias="fileInfo")


class GetFileByIdResponse(BaseModel):
    """Response containing a file with binary content."""

    file: File


class SaveFileRequest(BaseModel):
    """Request payload for uploading a file to a record field."""

    model_config = ConfigDict(populate_by_name=True)

    record_id: int = Field(alias="recordId")
    field_id: int = Field(alias="fieldId")
    file_name: str = Field(alias="fileName")
    file_path: str = Field(alias="filePath")
    content_type: str = Field(alias="contentType")
    notes: Optional[str] = None
    modified_date: Optional[datetime] = Field(default=None, alias="modifiedDate")


class SaveFileResponse(BaseModel):
    """Response containing the ID of a saved file."""

    id: int
