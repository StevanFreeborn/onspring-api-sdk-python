import pytest

from onspring_api_sdk.models import SaveFileRequest

pytestmark = pytest.mark.integration


def _attachment_path(testdata_dir):
    return str(testdata_dir / "test-attachment.txt")


def _image_path(testdata_dir):
    return str(testdata_dir / "test-image.jpeg")


class TestGetFileInfoById:
    @pytest.mark.flaky(reruns=3)
    def test_attachment_field(self, client, test_record, test_attachment_field, test_attachment):
        response = client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_attachment_field,
            file_id=test_attachment,
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.file_info.created_date is not None
        assert response.data.file_info.content_type is not None
        assert response.data.file_info.file_href is not None
        assert response.data.file_info.name is not None
        assert response.data.file_info.modified_date is not None
        assert response.data.file_info.type is not None
        assert response.data.file_info.owner is not None

    @pytest.mark.flaky(reruns=3)
    async def test_attachment_field_async(self, async_client, test_record, test_attachment_field, test_attachment):
        response = await async_client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_attachment_field,
            file_id=test_attachment,
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_image_field(self, client, test_record, test_image_field, test_image):
        response = client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_image_field,
            file_id=test_image,
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.file_info.created_date is not None
        assert response.data.file_info.content_type is not None
        assert response.data.file_info.file_href is not None
        assert response.data.file_info.name is not None
        assert response.data.file_info.modified_date is not None
        assert response.data.file_info.type is not None
        assert response.data.file_info.owner is not None

    @pytest.mark.flaky(reruns=3)
    async def test_image_field_async(self, async_client, test_record, test_image_field, test_image):
        response = await async_client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_image_field,
            file_id=test_image,
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_non_file_field_returns_400(self, client, test_record, test_text_field, test_attachment):
        response = client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_text_field,
            file_id=test_attachment,
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_non_file_field_returns_400_async(self, async_client, test_record, test_text_field, test_attachment):
        response = await async_client.get_file_info_by_id(
            record_id=test_record,
            field_id=test_text_field,
            file_id=test_attachment,
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url, test_record, test_attachment_field, test_attachment):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_file_info_by_id(
            record_id=test_record,
            field_id=test_attachment_field,
            file_id=test_attachment,
        )

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(
        self, base_url, test_record, test_attachment_field, test_attachment
    ):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_file_info_by_id(
            record_id=test_record,
            field_id=test_attachment_field,
            file_id=test_attachment,
        )

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_field_access_returns_403(self, client, test_attachment_field_no_access_field):
        response = client.get_file_info_by_id(record_id=1, field_id=test_attachment_field_no_access_field, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_field_access_returns_403_async(self, async_client, test_attachment_field_no_access_field):
        response = await async_client.get_file_info_by_id(
            record_id=1, field_id=test_attachment_field_no_access_field, file_id=1
        )

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_app_access_returns_403(self, client, test_attachment_field_no_access_app):
        response = client.get_file_info_by_id(record_id=1, field_id=test_attachment_field_no_access_app, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_app_access_returns_403_async(self, async_client, test_attachment_field_no_access_app):
        response = await async_client.get_file_info_by_id(
            record_id=1, field_id=test_attachment_field_no_access_app, file_id=1
        )

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_field_not_found_returns_404(self, client):
        response = client.get_file_info_by_id(record_id=1, field_id=0, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_field_not_found_returns_404_async(self, async_client):
        response = await async_client.get_file_info_by_id(record_id=1, field_id=0, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_attachment_field):
        response = client.get_file_info_by_id(record_id=0, field_id=test_attachment_field, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_record_not_found_returns_404_async(self, async_client, test_attachment_field):
        response = await async_client.get_file_info_by_id(record_id=0, field_id=test_attachment_field, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestGetFileById:
    @pytest.mark.flaky(reruns=3)
    def test_attachment_field(self, client, test_record, test_attachment_field, test_attachment):
        response = client.get_file_by_id(record_id=test_record, field_id=test_attachment_field, file_id=test_attachment)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.file.content_length is not None
        assert response.data.file.content_type is not None
        assert response.data.file.name is not None
        assert response.data.file.content is not None

    @pytest.mark.flaky(reruns=3)
    async def test_attachment_field_async(self, async_client, test_record, test_attachment_field, test_attachment):
        response = await async_client.get_file_by_id(
            record_id=test_record, field_id=test_attachment_field, file_id=test_attachment
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_image_field(self, client, test_record, test_image_field, test_image):
        response = client.get_file_by_id(record_id=test_record, field_id=test_image_field, file_id=test_image)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.file.content_length is not None
        assert response.data.file.content_type is not None
        assert response.data.file.name is not None
        assert response.data.file.content is not None

    @pytest.mark.flaky(reruns=3)
    async def test_image_field_async(self, async_client, test_record, test_image_field, test_image):
        response = await async_client.get_file_by_id(
            record_id=test_record, field_id=test_image_field, file_id=test_image
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_non_file_field_returns_400(self, client, test_record, test_text_field, test_attachment):
        response = client.get_file_by_id(record_id=test_record, field_id=test_text_field, file_id=test_attachment)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_non_file_field_returns_400_async(self, async_client, test_record, test_text_field, test_attachment):
        response = await async_client.get_file_by_id(
            record_id=test_record, field_id=test_text_field, file_id=test_attachment
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url, test_record, test_attachment_field, test_attachment):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_file_by_id(record_id=test_record, field_id=test_attachment_field, file_id=test_attachment)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(
        self, base_url, test_record, test_attachment_field, test_attachment
    ):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_file_by_id(
            record_id=test_record, field_id=test_attachment_field, file_id=test_attachment
        )

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_field_access_returns_403(self, client, test_attachment_field_no_access_field):
        response = client.get_file_by_id(record_id=1, field_id=test_attachment_field_no_access_field, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_field_access_returns_403_async(self, async_client, test_attachment_field_no_access_field):
        response = await async_client.get_file_by_id(
            record_id=1, field_id=test_attachment_field_no_access_field, file_id=1
        )

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_app_access_returns_403(self, client, test_attachment_field_no_access_app):
        response = client.get_file_by_id(record_id=1, field_id=test_attachment_field_no_access_app, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_app_access_returns_403_async(self, async_client, test_attachment_field_no_access_app):
        response = await async_client.get_file_by_id(
            record_id=1, field_id=test_attachment_field_no_access_app, file_id=1
        )

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_field_not_found_returns_404(self, client):
        response = client.get_file_by_id(record_id=1, field_id=0, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_field_not_found_returns_404_async(self, async_client):
        response = await async_client.get_file_by_id(record_id=1, field_id=0, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_attachment_field):
        response = client.get_file_by_id(record_id=0, field_id=test_attachment_field, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_record_not_found_returns_404_async(self, async_client, test_attachment_field):
        response = await async_client.get_file_by_id(record_id=0, field_id=test_attachment_field, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestSaveFile:
    _attachment_file_ids: list[int] = []

    @pytest.fixture(autouse=True)
    def cleanup_attachments(self, client, test_record, test_attachment_field):
        yield

        for file_id in self._attachment_file_ids:
            client.delete_file_by_id(record_id=test_record, field_id=test_attachment_field, file_id=file_id)

        self._attachment_file_ids.clear()

    @pytest.mark.flaky(reruns=3)
    def test_attachment_field(self, client, test_record, test_attachment_field, testdata_dir):
        request = SaveFileRequest(
            record_id=test_record,
            field_id=test_attachment_field,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
            notes="integration test",
        )

        response = client.save_file(request)

        assert response.status_code == 201
        assert response.is_successful
        assert response.data is not None
        assert response.data.id is not None

        self._attachment_file_ids.append(response.data.id)

    @pytest.mark.flaky(reruns=3)
    async def test_attachment_field_async(self, async_client, test_record, test_attachment_field, testdata_dir):
        request = SaveFileRequest(
            record_id=test_record,
            field_id=test_attachment_field,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
            notes="integration test",
        )

        response = await async_client.save_file(request)

        assert response.status_code == 201
        assert response.is_successful
        assert response.data is not None
        assert response.data.id is not None

        self._attachment_file_ids.append(response.data.id)

    @pytest.mark.flaky(reruns=3)
    def test_image_field(self, client, test_record, test_image_field, testdata_dir):
        request = SaveFileRequest(
            record_id=test_record,
            field_id=test_image_field,
            file_name="test-image.jpeg",
            file_path=_image_path(testdata_dir),
            content_type="image/jpeg",
            notes="integration test",
        )

        response = client.save_file(request)

        assert response.status_code == 201
        assert response.is_successful
        assert response.data is not None
        assert response.data.id is not None

        self._attachment_file_ids.append(response.data.id)

    @pytest.mark.flaky(reruns=3)
    def test_non_file_field_returns_400(self, client, test_record, test_text_field, testdata_dir):
        request = SaveFileRequest(
            record_id=test_record,
            field_id=test_text_field,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
            notes="integration test",
        )

        response = client.save_file(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url, testdata_dir):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = SaveFileRequest(
            record_id=1,
            field_id=1,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
        )

        response = bad.save_file(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_field_access_returns_403(self, client, test_attachment_field_no_access_field, testdata_dir):
        request = SaveFileRequest(
            record_id=1,
            field_id=test_attachment_field_no_access_field,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
        )

        response = client.save_file(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_app_access_returns_403(self, client, test_attachment_field_no_access_app, testdata_dir):
        request = SaveFileRequest(
            record_id=1,
            field_id=test_attachment_field_no_access_app,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
        )

        response = client.save_file(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_field_not_found_returns_404(self, client, testdata_dir):
        request = SaveFileRequest(
            record_id=1,
            field_id=0,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
        )

        response = client.save_file(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_attachment_field, testdata_dir):
        request = SaveFileRequest(
            record_id=0,
            field_id=test_attachment_field,
            file_name="test-attachment.txt",
            file_path=_attachment_path(testdata_dir),
            content_type="text/plain",
        )

        response = client.save_file(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None


class TestDeleteFileById:
    _attachment_file_id: int | None = None
    _image_file_id: int | None = None

    @pytest.fixture(autouse=True)
    def setup_files(self, client, test_record, test_attachment_field, test_image_field, testdata_dir):
        if self._attachment_file_id is None:
            req = SaveFileRequest(
                record_id=test_record,
                field_id=test_attachment_field,
                file_name="test-attachment.txt",
                file_path=_attachment_path(testdata_dir),
                content_type="text/plain",
                notes="delete test",
            )

            resp = client.save_file(req)

            if resp.data is not None:
                self._attachment_file_id = resp.data.id

        if self._image_file_id is None:
            req = SaveFileRequest(
                record_id=test_record,
                field_id=test_image_field,
                file_name="test-image.jpeg",
                file_path=_image_path(testdata_dir),
                content_type="image/jpeg",
                notes="delete test",
            )

            resp = client.save_file(req)

            if resp.data is not None:
                self._image_file_id = resp.data.id

        yield

    @pytest.mark.flaky(reruns=3)
    def test_attachment_field(self, client, test_record, test_attachment_field):
        assert self._attachment_file_id is not None

        response = client.delete_file_by_id(
            record_id=test_record,
            field_id=test_attachment_field,
            file_id=self._attachment_file_id,
        )

        assert response.status_code == 204
        assert response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_image_field(self, client, test_record, test_image_field):
        assert self._image_file_id is not None

        response = client.delete_file_by_id(
            record_id=test_record,
            field_id=test_image_field,
            file_id=self._image_file_id,
        )

        assert response.status_code == 204
        assert response.is_successful
        assert response.message is not None

    @pytest.mark.flaky(reruns=3)
    def test_non_file_field_returns_400(self, client, test_record, test_text_field):
        response = client.delete_file_by_id(record_id=test_record, field_id=test_text_field, file_id=1)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.delete_file_by_id(record_id=1, field_id=1, file_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_field_access_returns_403(self, client, test_attachment_field_no_access_field):
        response = client.delete_file_by_id(record_id=1, field_id=test_attachment_field_no_access_field, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_app_access_returns_403(self, client, test_attachment_field_no_access_app):
        response = client.delete_file_by_id(record_id=1, field_id=test_attachment_field_no_access_app, file_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_field_not_found_returns_404(self, client):
        response = client.delete_file_by_id(record_id=1, field_id=0, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_attachment_field):
        response = client.delete_file_by_id(record_id=0, field_id=test_attachment_field, file_id=1)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None
