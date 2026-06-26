import pytest

from onspring_api_sdk.models import PagingRequest

pytestmark = pytest.mark.integration


class TestGetApps:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client):
        response = client.get_apps()

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.page_number is not None
        assert response.data.page_size is not None
        assert response.data.total_pages is not None
        assert response.data.total_records is not None
        assert response.data.apps is not None
        assert len(response.data.apps) > 0

        for app in response.data.apps:
            assert app.id is not None
            assert app.name is not None
            assert app.href is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client):
        response = await async_client.get_apps()

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.apps) > 0

    @pytest.mark.flaky(reruns=3)
    def test_with_paging_request(self, client):
        response = client.get_apps(paging_request=PagingRequest(page_number=1, page_size=1))

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.apps) <= 1

    @pytest.mark.flaky(reruns=3)
    async def test_with_paging_request_async(self, async_client):
        response = await async_client.get_apps(paging_request=PagingRequest(page_number=1, page_size=1))

        assert response.status_code == 200
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.apps) <= 1

    @pytest.mark.flaky(reruns=3)
    def test_invalid_page_size_returns_400(self, client):
        response = client.get_apps(paging_request=PagingRequest(page_number=1, page_size=-1))

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_page_size_returns_400_async(self, async_client):
        response = await async_client.get_apps(paging_request=PagingRequest(page_number=1, page_size=-1))

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_apps()

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_apps()

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None


class TestGetAppById:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_app_id):
        response = client.get_app_by_id(app_id=test_app_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.app.id == test_app_id
        assert response.data.app.name is not None
        assert response.data.app.href is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_app_id):
        response = await async_client.get_app_by_id(app_id=test_app_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.app.id == test_app_id

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_app_by_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_app_by_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        response = client.get_app_by_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access):
        response = await async_client.get_app_by_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_not_found_returns_404(self, client):
        response = client.get_app_by_id(app_id=0)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_not_found_returns_404_async(self, async_client):
        response = await async_client.get_app_by_id(app_id=0)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestGetAppsByIds:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_app_ids):
        response = client.get_apps_by_ids(app_ids=test_app_ids)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.apps is not None
        assert len(response.data.apps) == len(test_app_ids)

        for app in response.data.apps:
            assert app.id is not None
            assert app.name is not None
            assert app.href is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_app_ids):
        response = await async_client.get_apps_by_ids(app_ids=test_app_ids)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.apps) == len(test_app_ids)

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.get_apps_by_ids(app_ids=[1])

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_apps_by_ids(app_ids=[1])

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_ids_no_access):
        response = client.get_apps_by_ids(app_ids=test_app_ids_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_ids_no_access):
        response = await async_client.get_apps_by_ids(app_ids=test_app_ids_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None
