import pytest
import respx
from httpx import Response

from onspring_api_sdk import AsyncOnspringClient
from onspring_api_sdk.errors import (
    OnspringAuthenticationError,
    OnspringError,
    OnspringNotFoundError,
    OnspringRateLimitError,
)
from onspring_api_sdk.models import (
    AddOrUpdateListItemResponse,
    AddOrUpdateRecordResponse,
    ApiResponse,
    GetAppByIdResponse,
    GetAppsByIdsResponse,
    GetAppsResponse,
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
    Record,
    SaveFileRequest,
    SaveFileResponse,
)

from .conftest import (
    MOCK_APP,
    MOCK_APPS_BATCH_RESPONSE,
    MOCK_APPS_RESPONSE,
    MOCK_FIELD,
    MOCK_FIELDS_BATCH_RESPONSE,
    MOCK_FIELDS_RESPONSE,
    MOCK_FILE_INFO,
    MOCK_LIST_ITEM_RESPONSE,
    MOCK_MESSAGE_RESPONSE,
    MOCK_RECORD,
    MOCK_RECORDS_BATCH_RESPONSE,
    MOCK_RECORDS_RESPONSE,
    MOCK_REPORT_RESPONSE,
    MOCK_REPORTS_BY_APP_RESPONSE,
    MOCK_SAVE_FILE_RESPONSE,
    MOCK_SAVE_RECORD_RESPONSE,
    TEST_URL,
    create_temp_file,
)


def _mock_json(status: int, json: dict | list | None = None) -> Response:
    return Response(status, json=json)


def _assert_error(response: ApiResponse, status: int, message: str | None) -> None:
    assert response.status_code == status
    assert response.is_successful is False
    assert response.data is None
    assert response.message == message


class TestCanConnect:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Ping").mock(return_value=Response(200))

            assert await async_client.can_connect() is True

    async def test_failure(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Ping").mock(return_value=Response(401))

            assert await async_client.can_connect() is False

    async def test_async_context_manager(self, async_client: AsyncOnspringClient):
        async with async_client as cm:
            assert cm is async_client

        assert async_client.client.is_closed

    async def test_aclose(self, async_client: AsyncOnspringClient):
        await async_client.aclose()
        assert async_client.client.is_closed


class TestGetApps:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps").mock(return_value=Response(200, json=MOCK_APPS_RESPONSE))

            response = await async_client.get_apps()

            assert response.is_successful
            assert isinstance(response.data, GetAppsResponse)
            assert len(response.data.apps) == 2
            assert response.data.apps[0].name == "Test App"

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps").mock(return_value=Response(400))

            _assert_error(await async_client.get_apps(), 400, "Invalid paging information")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps").mock(return_value=Response(401))

            _assert_error(await async_client.get_apps(), 401, "Unauthorized request")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps").mock(return_value=Response(418))

            _assert_error(await async_client.get_apps(), 418, None)

    async def test_with_explicit_paging(self, async_client: AsyncOnspringClient):
        from onspring_api_sdk.models import PagingRequest

        with respx.mock:
            respx.get(f"{TEST_URL}/Apps").mock(return_value=Response(200, json=MOCK_APPS_RESPONSE))

            paging = PagingRequest(page_number=2, page_size=10)
            response = await async_client.get_apps(paging_request=paging)

            assert response.is_successful
            assert isinstance(response.data, GetAppsResponse)


class TestGetAppById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps/id/1").mock(return_value=Response(200, json=MOCK_APP))

            response = await async_client.get_app_by_id(1)

            assert response.is_successful
            assert isinstance(response.data, GetAppByIdResponse)
            assert response.data.app.id == 1
            assert response.data.app.name == "Test App"

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps/id/1").mock(return_value=Response(401))

            _assert_error(await async_client.get_app_by_id(1), 401, "Unauthorized request")

    async def test_403(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps/id/1").mock(return_value=Response(403))

            _assert_error(await async_client.get_app_by_id(1), 403, "Client does not have read access to the app")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps/id/999").mock(return_value=Response(404))

            _assert_error(await async_client.get_app_by_id(999), 404, "App could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Apps/id/1").mock(return_value=Response(418))

            _assert_error(await async_client.get_app_by_id(1), 418, None)


class TestGetAppsByIds:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Apps/batch-get").mock(return_value=Response(200, json=MOCK_APPS_BATCH_RESPONSE))

            response = await async_client.get_apps_by_ids([1, 2])

            assert response.is_successful
            assert isinstance(response.data, GetAppsByIdsResponse)
            assert response.data.count == 2

    async def test_type_check(self, async_client: AsyncOnspringClient):
        response = await async_client.get_apps_by_ids("not a list")

        _assert_error(response, 400, "App ids should be of type list or tuple")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Apps/batch-get").mock(return_value=Response(401))

            _assert_error(await async_client.get_apps_by_ids([1]), 401, "Unauthorized request")

    async def test_403(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Apps/batch-get").mock(return_value=Response(403))

            _assert_error(await async_client.get_apps_by_ids([1]), 403, "Client does not have read access to the app")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Apps/batch-get").mock(return_value=Response(418))

            _assert_error(await async_client.get_apps_by_ids([1]), 418, None)


class TestGetFieldById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/id/1").mock(return_value=Response(200, json=MOCK_FIELD))

            response = await async_client.get_field_by_id(1)

            assert response.is_successful
            assert isinstance(response.data, GetFieldByIdResponse)
            assert response.data.field.id == 1
            assert response.data.field.name == "Test Field"

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/id/1").mock(return_value=Response(401))

            _assert_error(await async_client.get_field_by_id(1), 401, "Unauthorized request")

    async def test_403(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/id/1").mock(return_value=Response(403))

            _assert_error(await async_client.get_field_by_id(1), 403, "Client does not have read access to the field")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/id/999").mock(return_value=Response(404))

            _assert_error(await async_client.get_field_by_id(999), 404, "Field could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/id/1").mock(return_value=Response(418))

            _assert_error(await async_client.get_field_by_id(1), 418, None)


class TestGetFieldsByIds:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Fields/batch-get").mock(return_value=Response(200, json=MOCK_FIELDS_BATCH_RESPONSE))

            response = await async_client.get_fields_by_ids([1, 2])

            assert response.is_successful
            assert isinstance(response.data, GetFieldsByIdsResponse)
            assert response.data.count == 2

    async def test_type_check(self, async_client: AsyncOnspringClient):
        response = await async_client.get_fields_by_ids("not a list")

        _assert_error(response, 400, "Field ids should be of type list or tuple")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Fields/batch-get").mock(return_value=Response(401))

            _assert_error(await async_client.get_fields_by_ids([1]), 401, "Unauthorized request")

    async def test_403(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Fields/batch-get").mock(return_value=Response(403))

            _assert_error(
                await async_client.get_fields_by_ids([1]), 403, "Client does not have read access to the field(s)"
            )

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Fields/batch-get").mock(return_value=Response(404))

            _assert_error(await async_client.get_fields_by_ids([1]), 404, "Field(s) could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Fields/batch-get").mock(return_value=Response(418))

            _assert_error(await async_client.get_fields_by_ids([1]), 418, None)


class TestGetFieldsByAppId:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/appId/1").mock(return_value=Response(200, json=MOCK_FIELDS_RESPONSE))

            response = await async_client.get_fields_by_app_id(1)

            assert response.is_successful
            assert isinstance(response.data, GetFieldsByAppIdResponse)
            assert len(response.data.fields) == 2
            assert response.data.fields[0].id == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/appId/1").mock(return_value=Response(400))

            _assert_error(await async_client.get_fields_by_app_id(1), 400, "Invalid paging information")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/appId/1").mock(return_value=Response(401))

            _assert_error(await async_client.get_fields_by_app_id(1), 401, "Unauthorized request")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/appId/1").mock(return_value=Response(418))

            _assert_error(await async_client.get_fields_by_app_id(1), 418, None)

    async def test_with_explicit_paging(self, async_client: AsyncOnspringClient):
        from onspring_api_sdk.models import PagingRequest

        with respx.mock:
            respx.get(f"{TEST_URL}/Fields/appId/1").mock(return_value=Response(200, json=MOCK_FIELDS_RESPONSE))

            paging = PagingRequest(page_number=2, page_size=10)
            response = await async_client.get_fields_by_app_id(1, paging_request=paging)

            assert response.is_successful
            assert isinstance(response.data, GetFieldsByAppIdResponse)


class TestGetFileInfoById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(
                return_value=Response(200, json=MOCK_FILE_INFO)
            )

            response = await async_client.get_file_info_by_id(1, 2, 3)

            assert response.is_successful
            assert isinstance(response.data, GetFileInfoByIdResponse)
            assert response.data.file_info.name == "test.txt"
            assert response.data.file_info.content_type == "text/plain"

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(400))

            _assert_error(
                await async_client.get_file_info_by_id(1, 2, 3), 400, "Request is invalid based on underlying data"
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(401))

            _assert_error(await async_client.get_file_info_by_id(1, 2, 3), 401, "Unauthorized request")

    async def test_403(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(403))

            _assert_error(
                await async_client.get_file_info_by_id(1, 2, 3), 403, "Client does not have read access to the file"
            )

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(404))

            _assert_error(await async_client.get_file_info_by_id(1, 2, 3), 404, "File could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(418))

            _assert_error(await async_client.get_file_info_by_id(1, 2, 3), 418, None)


class TestDeleteFileById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(204))

            response = await async_client.delete_file_by_id(1, 2, 3)

            assert response.is_successful
            assert response.status_code == 204
            assert response.message == "File deleted successfully"

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(400))

            _assert_error(
                await async_client.delete_file_by_id(1, 2, 3), 400, "Request is invalid based on underlying data"
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(401))

            _assert_error(await async_client.delete_file_by_id(1, 2, 3), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(
                return_value=Response(403, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.delete_file_by_id(1, 2, 3)

            _assert_error(response, 403, "An error occurred")

    async def test_404_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(
                return_value=Response(404, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.delete_file_by_id(1, 2, 3)

            _assert_error(response, 404, "An error occurred")

    async def test_500(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(500))

            _assert_error(
                await async_client.delete_file_by_id(1, 2, 3), 500, "File could not be deleted due to internal error"
            )

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3").mock(return_value=Response(418))

            _assert_error(await async_client.delete_file_by_id(1, 2, 3), 418, None)


class TestGetFileById:
    def _mock_file_response(self, headers: dict | None = None) -> Response:
        h = {
            "content-disposition": "filename=test.txt",
            "content-type": "text/plain",
            "content-length": "12",
        }

        if headers:
            h.update(headers)

        return Response(200, headers=h, content=b"Hello World!")

    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(
                return_value=self._mock_file_response()
            )

            response = await async_client.get_file_by_id(1, 2, 3)

            assert response.is_successful
            assert isinstance(response.data, GetFileByIdResponse)
            assert response.data.file.name == "test.txt"
            assert response.data.file.content_type == "text/plain"
            assert response.data.file.content_length == 12
            assert response.data.file.content == b"Hello World!"

    async def test_quoted_filename(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(
                return_value=self._mock_file_response({"content-disposition": 'attachment; filename="quoted.pdf"'})
            )

            response = await async_client.get_file_by_id(1, 2, 3)

            assert response.data.file.name == "quoted.pdf"

    async def test_success_onspring_fallback(self, async_client: AsyncOnspringClient):
        """When no content-disposition header, fall back to 'OnspringFile'."""
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(
                return_value=self._mock_file_response({"content-disposition": ""})
            )

            response = await async_client.get_file_by_id(1, 2, 3)

            assert response.data.file.name == "OnspringFile"

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(return_value=Response(400))

            _assert_error(
                await async_client.get_file_by_id(1, 2, 3), 400, "Request is invalid based on underlying data"
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(return_value=Response(401))

            _assert_error(await async_client.get_file_by_id(1, 2, 3), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(
                return_value=Response(403, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.get_file_by_id(1, 2, 3)

            _assert_error(response, 403, "An error occurred")

    async def test_404_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(
                return_value=Response(404, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.get_file_by_id(1, 2, 3)

            _assert_error(response, 404, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Files/recordId/1/fieldId/2/fileId/3/file").mock(return_value=Response(418))

            _assert_error(await async_client.get_file_by_id(1, 2, 3), 418, None)


class TestSaveFile:
    async def test_success(self, async_client: AsyncOnspringClient):
        file_path = create_temp_file()
        request = SaveFileRequest(
            recordId=1,
            fieldId=2,
            fileName="test.txt",
            filePath=str(file_path),
            contentType="text/plain",
        )

        with respx.mock:
            respx.post(f"{TEST_URL}/Files").mock(return_value=Response(201, json=MOCK_SAVE_FILE_RESPONSE))

            response = await async_client.save_file(request)

            assert response.is_successful
            assert response.status_code == 201
            assert isinstance(response.data, SaveFileResponse)
            assert response.data.id == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        file_path = create_temp_file()
        request = SaveFileRequest(
            recordId=1,
            fieldId=2,
            fileName="test.txt",
            filePath=str(file_path),
            contentType="text/plain",
        )

        with respx.mock:
            respx.post(f"{TEST_URL}/Files").mock(return_value=Response(400))

            _assert_error(await async_client.save_file(request), 400, "Request is invalid based on underlying data")

    async def test_401(self, async_client: AsyncOnspringClient):
        file_path = create_temp_file()
        request = SaveFileRequest(
            recordId=1,
            fieldId=2,
            fileName="test.txt",
            filePath=str(file_path),
            contentType="text/plain",
        )

        with respx.mock:
            respx.post(f"{TEST_URL}/Files").mock(return_value=Response(401))

            _assert_error(await async_client.save_file(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        file_path = create_temp_file()
        request = SaveFileRequest(
            recordId=1,
            fieldId=2,
            fileName="test.txt",
            filePath=str(file_path),
            contentType="text/plain",
        )

        with respx.mock:
            respx.post(f"{TEST_URL}/Files").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            response = await async_client.save_file(request)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        file_path = create_temp_file()
        request = SaveFileRequest(
            recordId=1,
            fieldId=2,
            fileName="test.txt",
            filePath=str(file_path),
            contentType="text/plain",
        )

        with respx.mock:
            respx.post(f"{TEST_URL}/Files").mock(return_value=Response(418))

            _assert_error(await async_client.save_file(request), 418, None)


class TestAddOrUpdateListItem:
    async def test_200_update(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Lists/id/100/items").mock(return_value=Response(200, json=MOCK_LIST_ITEM_RESPONSE))
            from onspring_api_sdk.models import ListItemRequest

            request = ListItemRequest(listId=100, name="Updated Item")
            response = await async_client.add_or_update_list_item(request)

            assert response.is_successful
            assert response.status_code == 200
            assert response.message == "Existing list value successfully updated"
            assert isinstance(response.data, AddOrUpdateListItemResponse)

    async def test_201_create(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Lists/id/100/items").mock(return_value=Response(201, json=MOCK_LIST_ITEM_RESPONSE))

            from onspring_api_sdk.models import ListItemRequest

            request = ListItemRequest(listId=100, name="New Item")
            response = await async_client.add_or_update_list_item(request)

            assert response.is_successful
            assert response.status_code == 201
            assert response.message == "New list value successfully added"
            assert isinstance(response.data, AddOrUpdateListItemResponse)

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Lists/id/100/items").mock(return_value=Response(401))

            from onspring_api_sdk.models import ListItemRequest

            request = ListItemRequest(listId=100, name="Item")

            _assert_error(await async_client.add_or_update_list_item(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Lists/id/100/items").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            from onspring_api_sdk.models import ListItemRequest

            request = ListItemRequest(listId=100, name="Item")
            response = await async_client.add_or_update_list_item(request)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Lists/id/100/items").mock(return_value=Response(418))

            from onspring_api_sdk.models import ListItemRequest

            request = ListItemRequest(listId=100, name="Item")

            _assert_error(await async_client.add_or_update_list_item(request), 418, None)


class TestDeleteListItem:
    async def test_success(self, async_client: AsyncOnspringClient):
        item_id = "2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84"

        with respx.mock:
            respx.delete(f"{TEST_URL}/Lists/id/100/itemId/{item_id}").mock(return_value=Response(204))

            response = await async_client.delete_list_item(100, item_id)

            assert response.is_successful
            assert response.status_code == 204
            assert response.message == "Item deleted successfully"

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Lists/id/100/itemId/test").mock(return_value=Response(401))

            _assert_error(await async_client.delete_list_item(100, "test"), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Lists/id/100/itemId/test").mock(
                return_value=Response(403, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.delete_list_item(100, "test")

            _assert_error(response, 403, "An error occurred")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Lists/id/100/itemId/test").mock(return_value=Response(404))

            _assert_error(await async_client.delete_list_item(100, "test"), 404, "List/item could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Lists/id/100/itemId/test").mock(return_value=Response(418))

            _assert_error(await async_client.delete_list_item(100, "test"), 418, None)


class TestGetRecordsByAppRequestDefaults:
    async def test_default_page_values(self):
        from onspring_api_sdk.models import GetRecordsByAppRequest

        request = GetRecordsByAppRequest(app_id=100)

        assert request.page_number == 1
        assert request.page_size == 50


class TestGetRecordsByAppId:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100").mock(return_value=Response(200, json=MOCK_RECORDS_RESPONSE))

            request = GetRecordsByAppRequest(app_id=100)

            response = await async_client.get_records_by_app_id(request)

            assert response.is_successful
            assert isinstance(response.data, GetRecordsResponse)
            assert len(response.data.records) == 1
            assert response.data.records[0].record_id == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100").mock(return_value=Response(400))

            request = GetRecordsByAppRequest(app_id=100)

            _assert_error(
                await async_client.get_records_by_app_id(request),
                400,
                "Invalid paging information/size of the data requested was too large.",
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100").mock(return_value=Response(401))

            request = GetRecordsByAppRequest(app_id=100)

            _assert_error(await async_client.get_records_by_app_id(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            request = GetRecordsByAppRequest(app_id=100)

            response = await async_client.get_records_by_app_id(request)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100").mock(return_value=Response(418))

            request = GetRecordsByAppRequest(app_id=100)

            _assert_error(await async_client.get_records_by_app_id(request), 418, None)


class TestGetRecordById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(200, json=MOCK_RECORD))

            request = GetRecordByIdRequest(app_id=100, record_id=1)

            response = await async_client.get_record_by_id(request)

            assert response.is_successful
            assert isinstance(response.data, Record)
            assert response.data.record_id == 1
            assert len(response.data.fields) == 2

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(401))

            request = GetRecordByIdRequest(app_id=100, record_id=1)

            _assert_error(await async_client.get_record_by_id(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100/recordId/1").mock(
                return_value=Response(403, json=MOCK_MESSAGE_RESPONSE)
            )

            request = GetRecordByIdRequest(app_id=100, record_id=1)

            response = await async_client.get_record_by_id(request)

            _assert_error(response, 403, "An error occurred")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100/recordId/999").mock(return_value=Response(404))

            request = GetRecordByIdRequest(app_id=100, record_id=999)

            _assert_error(await async_client.get_record_by_id(request), 404, "Record could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(418))

            request = GetRecordByIdRequest(app_id=100, record_id=1)

            _assert_error(await async_client.get_record_by_id(request), 418, None)


class TestDeleteRecordById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(204))

            response = await async_client.delete_record_by_id(100, 1)

            assert response.is_successful
            assert response.status_code == 204
            assert response.message == "Record deleted successfully"

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(401))

            _assert_error(await async_client.delete_record_by_id(100, 1), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Records/appId/100/recordId/1").mock(
                return_value=Response(403, json=MOCK_MESSAGE_RESPONSE)
            )

            response = await async_client.delete_record_by_id(100, 1)

            _assert_error(response, 403, "An error occurred")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Records/appId/100/recordId/999").mock(return_value=Response(404))

            _assert_error(await async_client.delete_record_by_id(100, 999), 404, "Record could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.delete(f"{TEST_URL}/Records/appId/100/recordId/1").mock(return_value=Response(418))

            _assert_error(await async_client.delete_record_by_id(100, 1), 418, None)


class TestGetRecordsByIds:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-get").mock(
                return_value=Response(200, json=MOCK_RECORDS_BATCH_RESPONSE)
            )

            from onspring_api_sdk.models import GetBatchRecordsRequest

            request = GetBatchRecordsRequest(app_id=100, recordIds=[1])

            response = await async_client.get_records_by_ids(request)

            assert response.is_successful
            assert isinstance(response.data, GetBatchRecordsResponse)
            assert response.data.count == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-get").mock(return_value=Response(400))

            from onspring_api_sdk.models import GetBatchRecordsRequest

            request = GetBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(
                await async_client.get_records_by_ids(request),
                400,
                "Batch request is invalid/size of the data requested was too large.",
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-get").mock(return_value=Response(401))

            from onspring_api_sdk.models import GetBatchRecordsRequest

            request = GetBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.get_records_by_ids(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-get").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            from onspring_api_sdk.models import GetBatchRecordsRequest

            request = GetBatchRecordsRequest(app_id=100, recordIds=[1])

            response = await async_client.get_records_by_ids(request)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-get").mock(return_value=Response(418))

            from onspring_api_sdk.models import GetBatchRecordsRequest

            request = GetBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.get_records_by_ids(request), 418, None)


class TestQueryRecordsRequestDefaults:
    async def test_default_page_values(self):
        from onspring_api_sdk.models import QueryRecordsRequest

        request = QueryRecordsRequest(app_id=100, filter="test")

        assert request.page_number == 1
        assert request.page_size == 50


class TestQueryRecords:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(200, json=MOCK_RECORDS_RESPONSE))

            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test")

            response = await async_client.query_records(request)

            assert response.is_successful
            assert isinstance(response.data, GetRecordsResponse)
            assert len(response.data.records) == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(400))

            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test")

            _assert_error(
                await async_client.query_records(request),
                400,
                "Query request is invalid/size of the data requested was too large.",
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(401))

            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test")

            _assert_error(await async_client.query_records(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))
            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test")

            response = await async_client.query_records(request)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(418))

            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test")

            _assert_error(await async_client.query_records(request), 418, None)

    async def test_request_body_excludes_page_params(self, async_client: AsyncOnspringClient):
        with respx.mock:
            route = respx.post(f"{TEST_URL}/Records/Query").mock(return_value=Response(200, json=MOCK_RECORDS_RESPONSE))

            from onspring_api_sdk.models import QueryRecordsRequest

            request = QueryRecordsRequest(app_id=100, filter="Test", page_number=2, page_size=10)
            await async_client.query_records(request)

            body = route.calls[0].request.content
            assert b"pageNumber" not in body
            assert b"pageSize" not in body


class TestAddOrUpdateRecord:
    def _make_record(self) -> Record:
        from onspring_api_sdk.models import StringFieldValue

        return Record(
            appId=100,
            fieldData=[StringFieldValue(fieldId=1, value="test")],
        )

    async def test_200_update(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(200, json=MOCK_SAVE_RECORD_RESPONSE))

            response = await async_client.add_or_update_record(self._make_record())

            assert response.is_successful
            assert response.status_code == 200
            assert response.message == "Record updated successfully"
            assert isinstance(response.data, AddOrUpdateRecordResponse)
            assert response.data.id == 1

    async def test_201_create(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(201, json=MOCK_SAVE_RECORD_RESPONSE))

            response = await async_client.add_or_update_record(self._make_record())

            assert response.is_successful
            assert response.status_code == 201
            assert response.message == "Record created successfully"
            assert isinstance(response.data, AddOrUpdateRecordResponse)
            assert response.data.id == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(400))

            _assert_error(await async_client.add_or_update_record(self._make_record()), 400, "Request data is invalid")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(401))

            _assert_error(await async_client.add_or_update_record(self._make_record()), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            response = await async_client.add_or_update_record(self._make_record())

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(418))

            _assert_error(await async_client.add_or_update_record(self._make_record()), 418, None)

    async def test_with_guid_field(self, async_client: AsyncOnspringClient):
        import uuid

        from onspring_api_sdk.models import GuidFieldValue, Record

        record = Record(
            appId=100,
            fieldData=[GuidFieldValue(fieldId=1, value=uuid.UUID("12345678-1234-5678-1234-567812345678"))],
        )

        with respx.mock:
            respx.put(f"{TEST_URL}/Records").mock(return_value=Response(200, json=MOCK_SAVE_RECORD_RESPONSE))
            response = await async_client.add_or_update_record(record)

            assert response.is_successful

    async def test_payload_excludes_field_data(self, async_client: AsyncOnspringClient):
        from onspring_api_sdk.models import Record, StringFieldValue

        record = Record(
            appId=100,
            fieldData=[StringFieldValue(fieldId=1, value="test")],
        )

        with respx.mock:
            route = respx.put(f"{TEST_URL}/Records").mock(return_value=Response(200, json=MOCK_SAVE_RECORD_RESPONSE))
            await async_client.add_or_update_record(record)

            body = route.calls[0].request.content
            assert b"fieldData" not in body


class TestDeleteRecordsByIds:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(204))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1, 2])

            response = await async_client.delete_records_by_ids(request)

            assert response.is_successful
            assert response.status_code == 204
            assert response.message == "Record(s) deleted successfully"

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(400))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.delete_records_by_ids(request), 400, "Invalid request provided")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(401))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.delete_records_by_ids(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1])

            response = await async_client.delete_records_by_ids(request)

            _assert_error(response, 403, "An error occurred")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(404))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.delete_records_by_ids(request), 404, "Records could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.post(f"{TEST_URL}/Records/batch-delete").mock(return_value=Response(418))

            from onspring_api_sdk.models import DeleteBatchRecordsRequest

            request = DeleteBatchRecordsRequest(app_id=100, recordIds=[1])

            _assert_error(await async_client.delete_records_by_ids(request), 418, None)


class TestGetReportById:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(200, json=MOCK_REPORT_RESPONSE))

            request = GetReportByIdRequest(report_id=53)

            response = await async_client.get_report_by_id(request)

            assert response.is_successful
            assert isinstance(response.data, GetReportByIdResponse)
            assert len(response.data.columns) == 2
            assert len(response.data.rows) == 1
            assert response.data.rows[0].record_id == 1

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(400))

            request = GetReportByIdRequest(report_id=53)

            _assert_error(await async_client.get_report_by_id(request), 400, "Invalid request based on underlying data")

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(401))

            request = GetReportByIdRequest(report_id=53)

            _assert_error(await async_client.get_report_by_id(request), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            request = GetReportByIdRequest(report_id=53)

            response = await async_client.get_report_by_id(request)

            _assert_error(response, 403, "An error occurred")

    async def test_404(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/999").mock(return_value=Response(404))

            request = GetReportByIdRequest(report_id=999)

            _assert_error(await async_client.get_report_by_id(request), 404, "Report could not be found")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(418))

            request = GetReportByIdRequest(report_id=53)

            _assert_error(await async_client.get_report_by_id(request), 418, None)

    async def test_params_excludes_report_id(self, async_client: AsyncOnspringClient):
        request = GetReportByIdRequest(report_id=53)

        with respx.mock:
            route = respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(200, json=MOCK_REPORT_RESPONSE))
            await async_client.get_report_by_id(request)

            assert "reportId" not in route.calls[0].request.url.params

    async def test_403_empty_body(self, async_client: AsyncOnspringClient):
        request = GetReportByIdRequest(report_id=53)

        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/id/53").mock(return_value=Response(403, content=b""))
            response = await async_client.get_report_by_id(request)

            assert response.status_code == 403
            assert response.is_successful is False


class TestGetReportsByAppId:
    async def test_success(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(
                return_value=Response(200, json=MOCK_REPORTS_BY_APP_RESPONSE)
            )

            response = await async_client.get_reports_by_app_id(10)

            assert response.is_successful
            assert isinstance(response.data, GetReportsByAppIdResponse)
            assert len(response.data.reports) == 1
            assert response.data.reports[0].id == 53

    async def test_400(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(return_value=Response(400))

            _assert_error(
                await async_client.get_reports_by_app_id(10), 400, "Client does not have read access to the app."
            )

    async def test_401(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(return_value=Response(401))

            _assert_error(await async_client.get_reports_by_app_id(10), 401, "Unauthorized request")

    async def test_403_with_message(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(return_value=Response(403, json=MOCK_MESSAGE_RESPONSE))

            response = await async_client.get_reports_by_app_id(10)

            _assert_error(response, 403, "An error occurred")

    async def test_fallthrough(self, async_client: AsyncOnspringClient):
        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(return_value=Response(418))

            _assert_error(await async_client.get_reports_by_app_id(10), 418, None)

    async def test_with_explicit_paging(self, async_client: AsyncOnspringClient):
        from onspring_api_sdk.models import PagingRequest

        with respx.mock:
            respx.get(f"{TEST_URL}/Reports/appId/10").mock(
                return_value=Response(200, json=MOCK_REPORTS_BY_APP_RESPONSE)
            )

            paging = PagingRequest(page_number=2, page_size=10)
            response = await async_client.get_reports_by_app_id(10, paging_request=paging)

            assert response.is_successful
            assert isinstance(response.data, GetReportsByAppIdResponse)


class TestRaiseForStatus:
    async def test_401_raises_authentication_error(self):
        response = ApiResponse(status_code=401, message="Unauthorized")

        with pytest.raises(OnspringAuthenticationError, match="Unauthorized"):
            response.raise_for_status()

    async def test_403_raises_authentication_error(self):
        response = ApiResponse(status_code=403, message="Forbidden")

        with pytest.raises(OnspringAuthenticationError, match="Forbidden"):
            response.raise_for_status()

    async def test_404_raises_not_found_error(self):
        response = ApiResponse(status_code=404, message="Not Found")

        with pytest.raises(OnspringNotFoundError, match="Not Found"):
            response.raise_for_status()

    async def test_429_raises_rate_limit_error(self):
        response = ApiResponse(status_code=429, message="Rate limited")

        with pytest.raises(OnspringRateLimitError, match="Rate limited"):
            response.raise_for_status()

    async def test_418_raises_generic_error(self):
        response = ApiResponse(status_code=418, message="Teapot")

        with pytest.raises(OnspringError, match="Teapot"):
            response.raise_for_status()

    async def test_success_does_not_raise(self):
        response = ApiResponse(status_code=200, data="ok")
        response.raise_for_status()
