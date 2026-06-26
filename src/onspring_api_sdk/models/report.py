"""Pydantic models for Onspring report API requests and responses."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from onspring_api_sdk.enums import DataFormat, ReportDataType


class Row(BaseModel):
    """A single row of report data."""

    model_config = ConfigDict(populate_by_name=True)

    record_id: Optional[int] = Field(alias="recordId", default=None)
    cells: list[Any]


class Report(BaseModel):
    """Represents an Onspring report."""

    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    id: int
    name: str
    description: Optional[str] = None


class GetReportByIdRequest(BaseModel):
    """Request parameters for fetching a report by ID."""

    model_config = ConfigDict(populate_by_name=True)

    report_id: int = Field(alias="reportId")
    api_data_format: str = Field(default=DataFormat.Raw.name, alias="apiDataFormat")
    data_type: str = Field(default=ReportDataType.ReportData.name, alias="dataType")


class GetReportByIdResponse(BaseModel):
    """Response containing report columns and rows."""

    columns: list[str]
    rows: list[Row]


class GetReportsByAppIdResponse(BaseModel):
    """Paginated response containing reports for an app."""

    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_records: int = Field(alias="totalRecords")
    reports: list[Report] = Field(alias="items")
