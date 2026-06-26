import pytest

pytestmark = pytest.mark.integration


class TestCanConnect:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client):
        result = client.can_connect()
        assert result is True

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client):
        result = await async_client.can_connect()
        assert result is True
