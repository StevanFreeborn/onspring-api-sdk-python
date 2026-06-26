"""Pydantic models for Onspring record data, requests, and responses."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, Tag

from onspring_api_sdk.enums import DataFormat


class RecordFieldValue(BaseModel):
    """Base model for all record field value types."""

    model_config = ConfigDict(populate_by_name=True)

    field_id: int = Field(alias="fieldId")
    value: object = None
    type: str


class StringFieldValue(RecordFieldValue):
    """Field value containing a string."""

    type: Literal["String"] = "String"
    value: Optional[str] = None


class IntegerFieldValue(RecordFieldValue):
    """Field value containing an integer."""

    type: Literal["Integer"] = "Integer"
    value: Optional[int] = None


class DecimalFieldValue(RecordFieldValue):
    """Field value containing a decimal number."""

    type: Literal["Decimal"] = "Decimal"
    value: Optional[Decimal] = None


class DateFieldValue(RecordFieldValue):
    """Field value containing a date."""

    type: Literal["Date"] = "Date"
    value: Optional[datetime] = None


class GuidFieldValue(RecordFieldValue):
    """Field value containing a GUID."""

    type: Literal["Guid"] = "Guid"
    value: Optional[uuid.UUID] = None


class TimeSpanData(BaseModel):
    """Time span configuration with increment, recurrence, and end conditions."""

    model_config = ConfigDict(populate_by_name=True)

    quantity: Optional[Decimal] = None
    increment: Optional[str] = None
    recurrence: Optional[str] = None
    end_by_date: Optional[datetime] = Field(default=None, alias="endByDate")
    end_after_occurrences: Optional[int] = Field(default=None, alias="endAfterOccurrences")


class TimeSpanValue(RecordFieldValue):
    """Field value containing a time span."""

    type: Literal["TimeSpan"] = "TimeSpan"
    value: Optional[TimeSpanData] = None


class StringListValue(RecordFieldValue):
    """Field value containing a list of strings."""

    type: Literal["StringList"] = "StringList"
    value: Optional[list[str]] = None


class IntegerListValue(RecordFieldValue):
    """Field value containing a list of integers."""

    type: Literal["IntegerList"] = "IntegerList"
    value: Optional[list[int]] = None


class GuidListValue(RecordFieldValue):
    """Field value containing a list of GUIDs."""

    type: Literal["GuidList"] = "GuidList"
    value: Optional[list[uuid.UUID]] = None


class Attachment(BaseModel):
    """An attachment associated with a record field."""

    model_config = ConfigDict(populate_by_name=True)

    file_id: int = Field(alias="fileId")
    file_name: str = Field(alias="fileName")
    notes: Optional[str] = None
    storage_location: str = Field(alias="storageLocation")


class AttachmentListValue(RecordFieldValue):
    """Field value containing a list of attachments."""

    type: Literal["AttachmentList"] = "AttachmentList"
    value: Optional[list[Attachment]] = None


class ScoringGroup(BaseModel):
    """A scoring group with a list value reference, name, and scores."""

    model_config = ConfigDict(populate_by_name=True)

    list_value_id: Optional[uuid.UUID] = Field(default=None, alias="listValueId")
    name: Optional[str] = None
    score: Optional[Decimal] = None
    maximum_score: Optional[Decimal] = Field(default=None, alias="maximumScore")
    delegate_type: Optional[str] = Field(default=None, alias="delegateType")


class ScoringGroupListValue(RecordFieldValue):
    """Field value containing a list of scoring groups."""

    type: Literal["ScoringGroupList"] = "ScoringGroupList"
    value: Optional[list[ScoringGroup]] = None


class FileListValue(RecordFieldValue):
    """Field value containing a list of file IDs."""

    type: Literal["FileList"] = "FileList"
    value: Optional[list[int]] = None


FieldValue = Annotated[
    Union[
        Annotated[StringFieldValue, Tag("String")],
        Annotated[IntegerFieldValue, Tag("Integer")],
        Annotated[DecimalFieldValue, Tag("Decimal")],
        Annotated[DateFieldValue, Tag("Date")],
        Annotated[GuidFieldValue, Tag("Guid")],
        Annotated[TimeSpanValue, Tag("TimeSpan")],
        Annotated[StringListValue, Tag("StringList")],
        Annotated[IntegerListValue, Tag("IntegerList")],
        Annotated[GuidListValue, Tag("GuidList")],
        Annotated[AttachmentListValue, Tag("AttachmentList")],
        Annotated[ScoringGroupListValue, Tag("ScoringGroupList")],
        Annotated[FileListValue, Tag("FileList")],
    ],
    Field(discriminator="type"),
]


class Record(BaseModel):
    """A record containing typed field values for a specific app."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    record_id: Optional[int] = Field(default=None, alias="recordId")
    fields: list[FieldValue] = Field(default_factory=list, alias="fieldData")


class GetRecordsByAppRequest(BaseModel):
    """Request parameters for fetching records by app ID."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    field_ids: list[int] = Field(default_factory=list, alias="fieldIds")
    data_format: str = Field(default=DataFormat.Raw.name, alias="dataFormat")
    page_number: int = Field(default=1, alias="pageNumber")
    page_size: int = Field(default=50, alias="pageSize")


class QueryRecordsRequest(BaseModel):
    """Request parameters for querying records with a filter."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    filter: str
    field_ids: list[int] = Field(default_factory=list, alias="fieldIds")
    data_format: str = Field(default=DataFormat.Raw.name, alias="dataFormat")
    page_number: int = Field(default=1, alias="pageNumber")
    page_size: int = Field(default=50, alias="pageSize")


class GetRecordByIdRequest(BaseModel):
    """Request parameters for fetching a record by ID."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    record_id: int = Field(alias="recordId")
    field_ids: list[int] = Field(default_factory=list, alias="fieldIds")
    data_format: str = Field(default=DataFormat.Raw.name, alias="dataFormat")


class GetBatchRecordsRequest(BaseModel):
    """Request parameters for fetching multiple records by IDs."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    record_ids: list[int] = Field(alias="recordIds")
    field_ids: list[int] = Field(default_factory=list, alias="fieldIds")
    data_format: str = Field(default=DataFormat.Raw.name, alias="dataFormat")


class DeleteBatchRecordsRequest(BaseModel):
    """Request payload for deleting multiple records."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    record_ids: list[int] = Field(alias="recordIds")


class GetRecordsResponse(BaseModel):
    """Paginated response containing records."""

    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_records: int = Field(alias="totalRecords")
    records: list[Record] = Field(alias="items")


class GetBatchRecordsResponse(BaseModel):
    """Response containing records for requested IDs."""

    model_config = ConfigDict(populate_by_name=True)

    count: int
    records: list[Record] = Field(alias="items")


class AddOrUpdateRecordResponse(BaseModel):
    """Response containing the ID and warnings from an add/update operation."""

    id: int
    warnings: list[str] = Field(default_factory=list)
