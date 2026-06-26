"""Shared response handlers for Onspring API endpoints."""

import re

import httpx

from onspring_api_sdk.errors import _get_error_message
from onspring_api_sdk.models import (
    AddOrUpdateListItemResponse,
    AddOrUpdateRecordResponse,
    ApiResponse,
    App,
    File,
    FileInfo,
    GetAppByIdResponse,
    GetAppsByIdsResponse,
    GetAppsResponse,
    GetBatchRecordsResponse,
    GetFieldByIdResponse,
    GetFieldsByAppIdResponse,
    GetFieldsByIdsResponse,
    GetFileByIdResponse,
    GetFileInfoByIdResponse,
    GetRecordsResponse,
    GetReportByIdResponse,
    GetReportsByAppIdResponse,
    OnspringField,
    Record,
    SaveFileResponse,
)


def handle_get_apps_response(response: httpx.Response) -> ApiResponse[GetAppsResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Invalid paging information",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetAppsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_field_by_id_response(response: httpx.Response) -> ApiResponse[GetFieldByIdResponse]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the field",
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Field could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetFieldByIdResponse(field=OnspringField.model_validate(response.json())),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_fields_by_ids_response(response: httpx.Response) -> ApiResponse[GetFieldsByIdsResponse]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the field(s)",
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Field(s) could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetFieldsByIdsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_fields_by_app_id_response(response: httpx.Response) -> ApiResponse[GetFieldsByAppIdResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Invalid paging information",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetFieldsByAppIdResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_apps_by_ids_response(response: httpx.Response) -> ApiResponse[GetAppsByIdsResponse]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the app",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetAppsByIdsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_app_by_id_response(response: httpx.Response) -> ApiResponse[GetAppByIdResponse]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the app",
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="App could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetAppByIdResponse(app=App.model_validate(response.json())),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_file_info_by_id_response(response: httpx.Response) -> ApiResponse[GetFileInfoByIdResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Request is invalid based on underlying data",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the file",
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="File could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetFileInfoByIdResponse(file_info=FileInfo.model_validate(response.json())),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_delete_file_by_id_response(response: httpx.Response) -> ApiResponse[None]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Request is invalid based on underlying data",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403 | 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 500:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="File could not be deleted due to internal error",
                raw_response=response,
            )
        case 204:
            return ApiResponse(
                status_code=response.status_code, message="File deleted successfully", raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_file_by_id_response(response: httpx.Response) -> ApiResponse[GetFileByIdResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Request is invalid based on underlying data",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403 | 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200:
            headers = response.headers
            content_disposition = headers.get("content-disposition", "")
            match = re.search(r"filename=(.*?)(?:;|$)", content_disposition)
            file_name = match.group(1).strip("'\"") if match else "OnspringFile"
            file = File(
                name=file_name,
                contentType=headers.get("content-type", ""),
                contentLength=int(headers.get("content-length", 0)),
                content=response.content,
            )

            return ApiResponse(
                status_code=response.status_code, data=GetFileByIdResponse(file=file), raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_save_file_response(response: httpx.Response) -> ApiResponse[SaveFileResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Request is invalid based on underlying data",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403 | 404 | 500:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 201:
            return ApiResponse(
                status_code=response.status_code,
                data=SaveFileResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_add_or_update_list_item_response(
    response: httpx.Response,
) -> ApiResponse[AddOrUpdateListItemResponse]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403 | 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 201:
            return ApiResponse(
                status_code=response.status_code,
                data=AddOrUpdateListItemResponse.model_validate(response.json()),
                message="New list value successfully added",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=AddOrUpdateListItemResponse.model_validate(response.json()),
                message="Existing list value successfully updated",
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_delete_list_item_response(response: httpx.Response) -> ApiResponse[None]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="List/item could not be found",
                raw_response=response,
            )
        case 204:
            return ApiResponse(
                status_code=response.status_code, message="Item deleted successfully", raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_records_by_app_id_response(response: httpx.Response) -> ApiResponse[GetRecordsResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Invalid paging information/size of the data requested was too large.",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetRecordsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_record_by_id_response(response: httpx.Response) -> ApiResponse[Record]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Record could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code, data=Record.model_validate(response.json()), raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_delete_record_by_id_response(response: httpx.Response) -> ApiResponse[None]:
    match response.status_code:
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Record could not be found",
                raw_response=response,
            )
        case 204:
            return ApiResponse(
                status_code=response.status_code, message="Record deleted successfully", raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_records_by_ids_response(response: httpx.Response) -> ApiResponse[GetBatchRecordsResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Batch request is invalid/size of the data requested was too large.",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetBatchRecordsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_query_records_response(response: httpx.Response) -> ApiResponse[GetRecordsResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Query request is invalid/size of the data requested was too large.",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetRecordsResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_add_or_update_record_response(response: httpx.Response) -> ApiResponse[AddOrUpdateRecordResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Request data is invalid",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403 | 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200 | 201:
            message = "Record updated successfully" if response.status_code == 200 else "Record created successfully"
            return ApiResponse(
                status_code=response.status_code,
                data=AddOrUpdateRecordResponse.model_validate(response.json()),
                message=message,
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_delete_records_by_ids_response(response: httpx.Response) -> ApiResponse[None]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Invalid request provided",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Records could not be found",
                raw_response=response,
            )
        case 204:
            return ApiResponse(
                status_code=response.status_code, message="Record(s) deleted successfully", raw_response=response
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_report_by_id_response(response: httpx.Response) -> ApiResponse[GetReportByIdResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Invalid request based on underlying data",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 404:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Report could not be found",
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetReportByIdResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)


def handle_get_reports_by_app_id_response(response: httpx.Response) -> ApiResponse[GetReportsByAppIdResponse]:
    match response.status_code:
        case 400:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Client does not have read access to the app.",
                raw_response=response,
            )
        case 401:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message="Unauthorized request",
                raw_response=response,
            )
        case 403:
            return ApiResponse(
                status_code=response.status_code,
                is_successful=False,
                message=_get_error_message(response),
                raw_response=response,
            )
        case 200:
            return ApiResponse(
                status_code=response.status_code,
                data=GetReportsByAppIdResponse.model_validate(response.json()),
                raw_response=response,
            )
        case _:
            return ApiResponse(status_code=response.status_code, is_successful=False, raw_response=response)
