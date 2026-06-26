import pytest

from onspring_api_sdk.models import PagingRequest

pytestmark = pytest.mark.integration


class TestGetFieldById:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_field_id):
        response = client.get_field_by_id(field_id=test_field_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.field.id == test_field_id
        assert response.data.field.name is not None
        assert response.data.field.app_id is not None
        assert response.data.field.type is not None
        assert response.data.field.status is not None
        assert response.data.field.is_required is not None
        assert response.data.field.is_unique is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_field_id):
        response = await async_client.get_field_by_id(field_id=test_field_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.field.id == test_field_id

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_field_by_id(field_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_field_by_id(field_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_field_id_no_access):
        response = client.get_field_by_id(field_id=test_field_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_field_id_no_access):
        response = await async_client.get_field_by_id(field_id=test_field_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_not_found_returns_404(self, client):
        response = client.get_field_by_id(field_id=0)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_not_found_returns_404_async(self, async_client):
        response = await async_client.get_field_by_id(field_id=0)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestGetFieldsByAppId:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id):
        response = client.get_fields_by_app_id(app_id=test_survey_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.page_number is not None
        assert response.data.page_size is not None
        assert response.data.total_pages is not None
        assert response.data.total_records is not None
        assert response.data.fields is not None
        assert len(response.data.fields) > 0

        for field in response.data.fields:
            assert field.id is not None
            assert field.name is not None
            assert field.app_id is not None
            assert field.type is not None
            assert field.status is not None
            assert field.is_required is not None
            assert field.is_unique is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id):
        response = await async_client.get_fields_by_app_id(app_id=test_survey_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.fields) > 0

    @pytest.mark.flaky(reruns=3)
    def test_with_paging_request(self, client, test_survey_id):
        response = client.get_fields_by_app_id(
            app_id=test_survey_id,
            paging_request=PagingRequest(page_number=1, page_size=1),
        )

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.fields) <= 1

    @pytest.mark.flaky(reruns=3)
    async def test_with_paging_request_async(self, async_client, test_survey_id):
        response = await async_client.get_fields_by_app_id(
            app_id=test_survey_id,
            paging_request=PagingRequest(page_number=1, page_size=1),
        )

        assert response.status_code == 200
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.fields) <= 1

    @pytest.mark.flaky(reruns=3)
    def test_invalid_page_size_returns_400(self, client, test_survey_id):
        response = client.get_fields_by_app_id(
            app_id=test_survey_id,
            paging_request=PagingRequest(page_number=1, page_size=-1),
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_page_size_returns_400_async(self, async_client, test_survey_id):
        response = await async_client.get_fields_by_app_id(
            app_id=test_survey_id,
            paging_request=PagingRequest(page_number=1, page_size=-1),
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_fields_by_app_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_fields_by_app_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        response = client.get_fields_by_app_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access):
        response = await async_client.get_fields_by_app_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None


class TestGetFieldsByIds:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_field_ids):
        response = client.get_fields_by_ids(field_ids=test_field_ids)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.count == len(test_field_ids)
        assert len(response.data.fields) == len(test_field_ids)

        for field in response.data.fields:
            assert field.id is not None
            assert field.name is not None
            assert field.app_id is not None
            assert field.type is not None
            assert field.status is not None
            assert field.is_required is not None
            assert field.is_unique is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_field_ids):
        response = await async_client.get_fields_by_ids(field_ids=test_field_ids)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.count == len(test_field_ids)

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_fields_by_ids(field_ids=[1, 2, 3])

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_fields_by_ids(field_ids=[1, 2, 3])

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_field_ids_no_access):
        response = client.get_fields_by_ids(field_ids=test_field_ids_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_field_ids_no_access):
        response = await async_client.get_fields_by_ids(field_ids=test_field_ids_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None
