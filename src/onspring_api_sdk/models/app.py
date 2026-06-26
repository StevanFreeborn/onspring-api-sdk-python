"""Pydantic models for Onspring app API responses."""

from pydantic import BaseModel, ConfigDict, Field


class App(BaseModel):
    """Represents an Onspring app."""

    href: str
    id: int
    name: str


class GetAppsResponse(BaseModel):
    """Paginated response containing a list of apps."""

    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(alias="pageNumber")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_records: int = Field(alias="totalRecords")
    apps: list[App] = Field(alias="items")


class GetAppByIdResponse(BaseModel):
    """Response containing a single app."""

    app: App


class GetAppsByIdsResponse(BaseModel):
    """Response containing a list of apps for requested IDs."""

    model_config = ConfigDict(populate_by_name=True)

    count: int
    apps: list[App] = Field(alias="items")
