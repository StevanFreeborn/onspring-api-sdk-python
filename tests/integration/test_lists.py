import uuid

import pytest

from onspring_api_sdk.models import ListItemRequest

pytestmark = pytest.mark.integration


def _unique_name():
    return f"test_list_value_{uuid.uuid4().hex[:8]}"


class TestAddOrUpdateListItem:
    _new_item_ids: list[uuid.UUID] = []

    @pytest.fixture(autouse=True)
    def cleanup(self, client, test_list_id):
        yield

        for item_id in self._new_item_ids:
            client.delete_list_item(list_id=test_list_id, item_id=str(item_id))

        self._new_item_ids.clear()

    @pytest.mark.flaky(reruns=3)
    def test_add(self, client, test_list_id):
        request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        response = client.add_or_update_list_item(request)

        assert response.status_code == 201
        assert response.is_successful
        assert response.message is not None
        assert response.data is not None
        assert response.data.id is not None

        self._new_item_ids.append(response.data.id)

    @pytest.mark.flaky(reruns=3)
    async def test_add_async(self, async_client, test_list_id):
        request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        response = await async_client.add_or_update_list_item(request)

        assert response.status_code == 201
        assert response.is_successful
        assert response.data is not None
        assert response.data.id is not None

        if response.data.id:
            import os

            from onspring_api_sdk import OnspringClient

            sync = OnspringClient(os.environ["API_BASE_URL"], os.environ["SANDBOX_API_KEY"])
            sync.delete_list_item(list_id=test_list_id, item_id=str(response.data.id))

    @pytest.mark.flaky(reruns=3)
    def test_update(self, client, test_list_id):
        add_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        add_response = client.add_or_update_list_item(add_request)

        assert add_response.data is not None

        item_id = add_response.data.id
        self._new_item_ids.append(item_id)

        update_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            id=item_id,
            numeric_value=1,
            color="#000000",
        )

        update_response = client.add_or_update_list_item(update_request)

        assert update_response.status_code == 200
        assert update_response.is_successful
        assert update_response.message is not None
        assert update_response.data is not None

    @pytest.mark.flaky(reruns=3)
    async def test_update_async(self, async_client, test_list_id):
        add_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        add_response = await async_client.add_or_update_list_item(add_request)

        assert add_response.data is not None

        item_id = add_response.data.id

        import os

        from onspring_api_sdk import OnspringClient

        sync = OnspringClient(os.environ["API_BASE_URL"], os.environ["SANDBOX_API_KEY"])

        update_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            id=item_id,
            numeric_value=1,
            color="#000000",
        )

        update_response = await async_client.add_or_update_list_item(update_request)

        assert update_response.status_code == 200
        assert update_response.is_successful
        assert update_response.data is not None

        sync.delete_list_item(list_id=test_list_id, item_id=str(item_id))

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = ListItemRequest(list_id=1, name="test", numeric_value=1, color="#000000")

        response = bad.add_or_update_list_item(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client):
        request = ListItemRequest(list_id=1, name="test", numeric_value=1, color="#000000")

        response = client.add_or_update_list_item(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_list_not_found_returns_404(self, client):
        request = ListItemRequest(list_id=0, name="test", numeric_value=1, color="#000000")

        response = client.add_or_update_list_item(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_item_not_found_returns_404(self, client, test_list_id):
        request = ListItemRequest(
            list_id=test_list_id,
            id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            name="test",
        )

        response = client.add_or_update_list_item(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None


class TestDeleteListItem:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_list_id):
        add_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        add_response = client.add_or_update_list_item(add_request)

        assert add_response.data is not None

        item_id = str(add_response.data.id)

        response = client.delete_list_item(list_id=test_list_id, item_id=item_id)

        assert response.status_code == 204
        assert response.is_successful
        assert response.message is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_list_id):
        import os

        from onspring_api_sdk import OnspringClient

        sync = OnspringClient(os.environ["API_BASE_URL"], os.environ["SANDBOX_API_KEY"])

        add_request = ListItemRequest(
            list_id=test_list_id,
            name=_unique_name(),
            numeric_value=1,
            color="#000000",
        )

        add_response = sync.add_or_update_list_item(add_request)

        assert add_response.data is not None

        item_id = str(add_response.data.id)

        response = await async_client.delete_list_item(list_id=test_list_id, item_id=item_id)

        assert response.status_code == 204
        assert response.is_successful

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.delete_list_item(list_id=1, item_id="1")

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_list_id_no_access, test_list_item_id_no_access):
        response = client.delete_list_item(list_id=test_list_id_no_access, item_id=test_list_item_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_list_not_found_returns_404(self, client):
        response = client.delete_list_item(list_id=0, item_id="3fa85f64-5717-4562-b3fc-2c963f66afa6")

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_item_not_found_returns_404(self, client, test_list_id):
        response = client.delete_list_item(
            list_id=test_list_id,
            item_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        )

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None
