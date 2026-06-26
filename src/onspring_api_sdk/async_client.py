"""Async HTTP client for the Onspring API v2."""

import asyncio
import json
from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

import httpx

from onspring_api_sdk._responses import (
    handle_add_or_update_list_item_response,
    handle_add_or_update_record_response,
    handle_delete_file_by_id_response,
    handle_delete_list_item_response,
    handle_delete_record_by_id_response,
    handle_delete_records_by_ids_response,
    handle_get_app_by_id_response,
    handle_get_apps_by_ids_response,
    handle_get_apps_response,
    handle_get_field_by_id_response,
    handle_get_fields_by_app_id_response,
    handle_get_fields_by_ids_response,
    handle_get_file_by_id_response,
    handle_get_file_info_by_id_response,
    handle_get_record_by_id_response,
    handle_get_records_by_app_id_response,
    handle_get_records_by_ids_response,
    handle_get_report_by_id_response,
    handle_get_reports_by_app_id_response,
    handle_query_records_response,
    handle_save_file_response,
)
from onspring_api_sdk.endpoints import (
    add_or_update_list_item_endpoint,
    add_or_update_record_endpoint,
    delete_file_by_id_endpoint,
    delete_list_item_endpoint,
    delete_record_by_id_endpoint,
    delete_records_by_ids_endpoint,
    get_app_by_id_endpoint,
    get_apps_by_ids_endpoint,
    get_apps_endpoint,
    get_field_by_id_endpoint,
    get_fields_by_app_id_endpoint,
    get_fields_by_ids_endpoint,
    get_file_by_id_endpoint,
    get_file_info_by_id_endpoint,
    get_ping_endpoint,
    get_record_by_id_endpoint,
    get_records_by_app_id_endpoint,
    get_records_by_ids_endpoint,
    get_report_by_id_endpoint,
    get_reports_by_app_id_endpoint,
    query_records_endpoint,
    save_file_endpoint,
)
from onspring_api_sdk.models import (
    AddOrUpdateListItemResponse,
    AddOrUpdateRecordResponse,
    ApiResponse,
    DeleteBatchRecordsRequest,
    GetAppByIdResponse,
    GetAppsByIdsResponse,
    GetAppsResponse,
    GetBatchRecordsRequest,
    GetBatchRecordsResponse,
    GetFieldByIdResponse,
    GetFieldsByAppIdResponse,
    GetFieldsByIdsResponse,
    GetFileByIdResponse,
    GetFileInfoByIdResponse,
    GetRecordByIdRequest,
    GetRecordsByAppRequest,
    GetRecordsResponse,
    GetReportByIdRequest,
    GetReportByIdResponse,
    GetReportsByAppIdResponse,
    ListItemRequest,
    PagingRequest,
    QueryRecordsRequest,
    Record,
    SaveFileRequest,
    SaveFileResponse,
)

API_VERSION = "2"
CONTENT_TYPE_JSON = "application/json"
_JSON_HEADERS: Final[Mapping[str, str]] = MappingProxyType({"Content-Type": CONTENT_TYPE_JSON})


class AsyncOnspringClient:
    """Async client for interacting with the Onspring API v2."""

    def __init__(self, url: str, key: str):
        """Initialize the client with a base URL and API key."""
        self.client = httpx.AsyncClient(
            headers={
                "x-apikey": key,
                "x-api-version": API_VERSION,
            }
        )
        self.base_url = url

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self) -> "AsyncOnspringClient":
        """Enter the async runtime context for the client."""
        return self

    async def __aexit__(self, *args) -> None:
        """Exit the async runtime context and close the client."""
        await self.aclose()

    async def can_connect(self) -> bool:
        """Ping the API to check connectivity."""
        response = await self.client.get(get_ping_endpoint(self.base_url))

        return response.status_code == 200

    async def get_apps(self, paging_request: PagingRequest | None = None) -> ApiResponse[GetAppsResponse]:
        """Retrieve all apps the API key has access to."""
        if paging_request is None:
            paging_request = PagingRequest()

        response = await self.client.get(
            get_apps_endpoint(self.base_url),
            params=paging_request.model_dump(by_alias=True, exclude_none=True),
        )

        return handle_get_apps_response(response)

    async def get_app_by_id(self, app_id: int) -> ApiResponse[GetAppByIdResponse]:
        """Retrieve an app by its ID."""
        response = await self.client.get(get_app_by_id_endpoint(self.base_url, app_id))

        return handle_get_app_by_id_response(response)

    async def get_apps_by_ids(self, app_ids: list[int]) -> ApiResponse[GetAppsByIdsResponse]:
        """Retrieve multiple apps by their IDs."""
        if not isinstance(app_ids, (list, tuple)):
            return ApiResponse(status_code=400, is_successful=False, message="App ids should be of type list or tuple")

        response = await self.client.post(
            get_apps_by_ids_endpoint(self.base_url),
            content=json.dumps(app_ids),
            headers=_JSON_HEADERS,
        )

        return handle_get_apps_by_ids_response(response)

    async def get_field_by_id(self, field_id: int) -> ApiResponse[GetFieldByIdResponse]:
        """Retrieve a field by its ID."""
        response = await self.client.get(get_field_by_id_endpoint(self.base_url, field_id))

        return handle_get_field_by_id_response(response)

    async def get_fields_by_ids(self, field_ids: list[int]) -> ApiResponse[GetFieldsByIdsResponse]:
        """Retrieve multiple fields by their IDs."""
        if not isinstance(field_ids, (list, tuple)):
            return ApiResponse(
                status_code=400, is_successful=False, message="Field ids should be of type list or tuple"
            )

        response = await self.client.post(
            get_fields_by_ids_endpoint(self.base_url),
            content=json.dumps(field_ids),
            headers=_JSON_HEADERS,
        )

        return handle_get_fields_by_ids_response(response)

    async def get_fields_by_app_id(
        self, app_id: int, paging_request: PagingRequest | None = None
    ) -> ApiResponse[GetFieldsByAppIdResponse]:
        """Retrieve all fields for a given app."""
        if paging_request is None:
            paging_request = PagingRequest()

        response = await self.client.get(
            get_fields_by_app_id_endpoint(self.base_url, app_id),
            params=paging_request.model_dump(by_alias=True, exclude_none=True),
        )

        return handle_get_fields_by_app_id_response(response)

    async def get_file_info_by_id(
        self, record_id: int, field_id: int, file_id: int
    ) -> ApiResponse[GetFileInfoByIdResponse]:
        """Retrieve file metadata for a file attached to a record."""
        response = await self.client.get(get_file_info_by_id_endpoint(self.base_url, record_id, field_id, file_id))

        return handle_get_file_info_by_id_response(response)

    async def delete_file_by_id(self, record_id: int, field_id: int, file_id: int) -> ApiResponse[None]:
        """Delete a file attached to a record."""
        response = await self.client.delete(delete_file_by_id_endpoint(self.base_url, record_id, field_id, file_id))

        return handle_delete_file_by_id_response(response)

    async def get_file_by_id(self, record_id: int, field_id: int, file_id: int) -> ApiResponse[GetFileByIdResponse]:
        """Download a file attached to a record."""
        response = await self.client.get(get_file_by_id_endpoint(self.base_url, record_id, field_id, file_id))

        return handle_get_file_by_id_response(response)

    async def save_file(self, save_file_request: SaveFileRequest) -> ApiResponse[SaveFileResponse]:
        """Upload a file to a record."""
        endpoint = save_file_endpoint(self.base_url)

        def _read_file() -> bytes:
            with open(save_file_request.file_path, "rb") as f:
                return f.read()

        file_content = await asyncio.to_thread(_read_file)

        files = {
            "File": (
                save_file_request.file_name,
                file_content,
                save_file_request.content_type,
            ),
        }

        data = save_file_request.model_dump(
            by_alias=True, exclude={"file_name", "file_path", "content_type"}, exclude_none=True
        )

        response = await self.client.post(endpoint, data=data, files=files)

        return handle_save_file_response(response)

    async def add_or_update_list_item(
        self, list_item_request: ListItemRequest
    ) -> ApiResponse[AddOrUpdateListItemResponse]:
        """Add or update a list item value."""
        endpoint = add_or_update_list_item_endpoint(self.base_url, list_item_request.list_id)
        payload = list_item_request.model_dump(by_alias=True, exclude={"list_id"}, exclude_none=True, mode="json")

        response = await self.client.put(
            endpoint,
            content=json.dumps(payload),
            headers=_JSON_HEADERS,
        )

        return handle_add_or_update_list_item_response(response)

    async def delete_list_item(self, list_id: int, item_id: str) -> ApiResponse[None]:
        """Delete a list item by its ID."""
        response = await self.client.delete(delete_list_item_endpoint(self.base_url, list_id, item_id))

        return handle_delete_list_item_response(response)

    async def get_records_by_app_id(self, request: GetRecordsByAppRequest) -> ApiResponse[GetRecordsResponse]:
        """Retrieve records from an app with optional filtering and paging."""
        params = request.model_dump(by_alias=True, exclude={"app_id"}, exclude_none=True)
        field_ids = params.pop("fieldIds", None)

        if field_ids:
            params["fieldIds"] = ",".join(str(i) for i in field_ids)

        response = await self.client.get(
            get_records_by_app_id_endpoint(self.base_url, request.app_id),
            params=params,
        )

        return handle_get_records_by_app_id_response(response)

    async def get_record_by_id(self, request: GetRecordByIdRequest) -> ApiResponse[Record]:
        """Retrieve a single record by its ID."""
        params = request.model_dump(by_alias=True, exclude={"app_id", "record_id"}, exclude_none=True)
        field_ids = params.pop("fieldIds", None)

        if field_ids:
            params["fieldIds"] = ",".join(str(i) for i in field_ids)

        response = await self.client.get(
            get_record_by_id_endpoint(self.base_url, request.app_id, request.record_id),
            params=params,
        )

        return handle_get_record_by_id_response(response)

    async def delete_record_by_id(self, app_id: int, record_id: int) -> ApiResponse[None]:
        """Delete a single record by its ID."""
        response = await self.client.delete(delete_record_by_id_endpoint(self.base_url, app_id, record_id))

        return handle_delete_record_by_id_response(response)

    async def get_records_by_ids(self, request: GetBatchRecordsRequest) -> ApiResponse[GetBatchRecordsResponse]:
        """Retrieve multiple records by their IDs."""
        response = await self.client.post(
            get_records_by_ids_endpoint(self.base_url),
            content=json.dumps(request.model_dump(by_alias=True, exclude_none=True, mode="json")),
            headers=_JSON_HEADERS,
        )

        return handle_get_records_by_ids_response(response)

    async def query_records(self, request: QueryRecordsRequest) -> ApiResponse[GetRecordsResponse]:
        """Query records using a structured query."""
        exclude = {"page_number", "page_size"}
        payload = request.model_dump(by_alias=True, exclude=exclude, exclude_none=True, mode="json")
        params = {"pageNumber": request.page_number, "pageSize": request.page_size}

        response = await self.client.post(
            query_records_endpoint(self.base_url),
            content=json.dumps(payload),
            params=params,
            headers=_JSON_HEADERS,
        )

        return handle_query_records_response(response)

    async def add_or_update_record(self, record: Record) -> ApiResponse[AddOrUpdateRecordResponse]:
        """Add or update a record."""
        fields_dict = {}

        for field in record.fields:
            fields_dict[field.field_id] = field.value

        payload = record.model_dump(by_alias=True, exclude={"fields"}, exclude_none=True, mode="json")
        payload["fields"] = fields_dict

        response = await self.client.put(
            add_or_update_record_endpoint(self.base_url),
            content=json.dumps(payload, default=str),
            headers=_JSON_HEADERS,
        )

        return handle_add_or_update_record_response(response)

    async def delete_records_by_ids(self, request: DeleteBatchRecordsRequest) -> ApiResponse[None]:
        """Delete multiple records by their IDs."""
        response = await self.client.post(
            delete_records_by_ids_endpoint(self.base_url),
            content=json.dumps(request.model_dump(by_alias=True, exclude_none=True, mode="json")),
            headers=_JSON_HEADERS,
        )

        return handle_delete_records_by_ids_response(response)

    async def get_report_by_id(self, request: GetReportByIdRequest) -> ApiResponse[GetReportByIdResponse]:
        """Retrieve a report by its ID."""
        params = request.model_dump(by_alias=True, exclude={"report_id"}, exclude_none=True)

        response = await self.client.get(
            get_report_by_id_endpoint(self.base_url, request.report_id),
            params=params,
        )

        return handle_get_report_by_id_response(response)

    async def get_reports_by_app_id(
        self, app_id: int, paging_request: PagingRequest | None = None
    ) -> ApiResponse[GetReportsByAppIdResponse]:
        """Retrieve all reports for a given app."""
        if paging_request is None:
            paging_request = PagingRequest()

        response = await self.client.get(
            get_reports_by_app_id_endpoint(self.base_url, app_id),
            params=paging_request.model_dump(by_alias=True, exclude_none=True),
        )

        return handle_get_reports_by_app_id_response(response)
