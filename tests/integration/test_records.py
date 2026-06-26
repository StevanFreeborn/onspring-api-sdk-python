import pytest

from onspring_api_sdk.enums import DataFormat
from onspring_api_sdk.models import (
    DeleteBatchRecordsRequest,
    GetBatchRecordsRequest,
    GetRecordByIdRequest,
    GetRecordsByAppRequest,
    QueryRecordsRequest,
    Record,
    StringFieldValue,
)

pytestmark = pytest.mark.integration


class TestGetRecordsByAppId:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id):
        request = GetRecordsByAppRequest(app_id=test_survey_id)

        response = client.get_records_by_app_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.page_number is not None
        assert response.data.page_size is not None
        assert response.data.total_pages is not None
        assert response.data.total_records is not None
        assert response.data.records is not None

        for record in response.data.records:
            assert record.app_id == test_survey_id
            assert record.record_id is not None
            assert record.fields is not None
            assert len(record.fields) > 0

            for field in record.fields:
                assert field.field_id is not None
                assert field.type is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id):
        request = GetRecordsByAppRequest(app_id=test_survey_id)

        response = await async_client.get_records_by_app_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.records) > 0

    @pytest.mark.flaky(reruns=3)
    def test_with_params(self, client, test_survey_id, test_text_field):
        request = GetRecordsByAppRequest(
            app_id=test_survey_id,
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
            page_number=1,
            page_size=1,
        )

        response = client.get_records_by_app_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.records) == 1

    @pytest.mark.flaky(reruns=3)
    async def test_with_params_async(self, async_client, test_survey_id, test_text_field):
        request = GetRecordsByAppRequest(
            app_id=test_survey_id,
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
            page_number=1,
            page_size=1,
        )

        response = await async_client.get_records_by_app_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1
        assert len(response.data.records) == 1

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = GetRecordsByAppRequest(app_id=0)

        response = bad.get_records_by_app_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        request = GetRecordsByAppRequest(app_id=0)

        response = await bad.get_records_by_app_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        request = GetRecordsByAppRequest(app_id=test_app_id_no_access)

        response = client.get_records_by_app_id(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access):
        request = GetRecordsByAppRequest(app_id=test_app_id_no_access)

        response = await async_client.get_records_by_app_id(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None


class TestGetRecordById:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id, test_survey_record_id):
        request = GetRecordByIdRequest(app_id=test_survey_id, record_id=test_survey_record_id)

        response = client.get_record_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.app_id == test_survey_id
        assert response.data.record_id == test_survey_record_id
        assert response.data.fields is not None
        assert len(response.data.fields) > 0

        for field in response.data.fields:
            assert field.field_id is not None
            assert field.type is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id, test_survey_record_id):
        request = GetRecordByIdRequest(app_id=test_survey_id, record_id=test_survey_record_id)

        response = await async_client.get_record_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.app_id == test_survey_id
        assert response.data.record_id == test_survey_record_id

    @pytest.mark.flaky(reruns=3)
    def test_with_params(self, client, test_survey_id, test_survey_record_id, test_text_field):
        request = GetRecordByIdRequest(
            app_id=test_survey_id,
            record_id=test_survey_record_id,
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
        )

        response = client.get_record_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.app_id == test_survey_id
        assert response.data.record_id == test_survey_record_id
        assert len(response.data.fields) > 0

    @pytest.mark.flaky(reruns=3)
    async def test_with_params_async(self, async_client, test_survey_id, test_survey_record_id, test_text_field):
        request = GetRecordByIdRequest(
            app_id=test_survey_id,
            record_id=test_survey_record_id,
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
        )

        response = await async_client.get_record_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = GetRecordByIdRequest(app_id=1, record_id=1)

        response = bad.get_record_by_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        request = GetRecordByIdRequest(app_id=1, record_id=1)

        response = await bad.get_record_by_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_survey_id):
        request = GetRecordByIdRequest(app_id=test_survey_id, record_id=0)

        response = client.get_record_by_id(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_record_not_found_returns_404_async(self, async_client, test_survey_id):
        request = GetRecordByIdRequest(app_id=test_survey_id, record_id=0)

        response = await async_client.get_record_by_id(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestSaveRecord:
    _new_records: list[dict] = []

    @pytest.fixture(autouse=True)
    def cleanup(self, client):
        yield

        for rec in self._new_records:
            client.delete_record_by_id(app_id=rec["app_id"], record_id=rec["record_id"])

        self._new_records.clear()

    @pytest.mark.flaky(reruns=3)
    def test_add(self, client, test_survey_id, test_text_field):
        record = Record(
            app_id=test_survey_id,
            fields=[StringFieldValue(field_id=test_text_field, value="Test")],
        )

        response = client.add_or_update_record(record)

        assert response.status_code == 201
        assert response.is_successful
        assert response.message is not None
        assert response.data is not None
        assert response.data.id is not None
        assert response.data.warnings is not None

        self._new_records.append({"app_id": test_survey_id, "record_id": response.data.id})

    @pytest.mark.flaky(reruns=3)
    async def test_add_async(self, async_client, test_survey_id, test_text_field):
        record = Record(
            app_id=test_survey_id,
            fields=[StringFieldValue(field_id=test_text_field, value="Test")],
        )

        response = await async_client.add_or_update_record(record)

        assert response.status_code == 201
        assert response.is_successful
        assert response.data is not None
        assert response.data.id is not None
        self._new_records.append({"app_id": test_survey_id, "record_id": response.data.id})

        if response.data.id:
            import os

            from onspring_api_sdk import OnspringClient

            sync = OnspringClient(os.environ["API_BASE_URL"], os.environ["SANDBOX_API_KEY"])
            sync.delete_record_by_id(app_id=test_survey_id, record_id=response.data.id)

    @pytest.mark.flaky(reruns=3)
    def test_update(self, client, test_survey_id, test_text_field):
        new_record = Record(
            app_id=test_survey_id,
            fields=[StringFieldValue(field_id=test_text_field, value="Test")],
        )

        new_response = client.add_or_update_record(new_record)

        assert new_response.data is not None

        new_id = new_response.data.id

        self._new_records.append({"app_id": test_survey_id, "record_id": new_id})

        update_record = Record(
            app_id=test_survey_id,
            record_id=new_id,
            fields=[StringFieldValue(field_id=test_text_field, value="updated")],
        )

        response = client.add_or_update_record(update_record)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.id == new_id
        assert response.data.warnings is not None

    @pytest.mark.flaky(reruns=3)
    def test_empty_fields_returns_400(self, client, test_survey_id):
        record = Record(app_id=test_survey_id, fields=[])

        response = client.add_or_update_record(record)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        record = Record(app_id=0, fields=[])

        response = bad.add_or_update_record(record)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        record = Record(app_id=test_app_id_no_access, fields=[])

        response = client.add_or_update_record(record)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_survey_id):
        record = Record(app_id=test_survey_id, record_id=0, fields=[])

        response = client.add_or_update_record(record)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None


class TestDeleteRecordById:
    def _create_temp_record(self, client, test_survey_id, test_text_field):
        record = Record(
            app_id=test_survey_id,
            fields=[StringFieldValue(field_id=test_text_field, value="to_delete")],
        )

        response = client.add_or_update_record(record)

        assert response.data is not None
        return response.data.id

    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id, test_text_field):
        record_id = self._create_temp_record(client, test_survey_id, test_text_field)

        response = client.delete_record_by_id(app_id=test_survey_id, record_id=record_id)

        assert response.status_code == 204
        assert response.is_successful

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id, test_text_field):
        import os

        from onspring_api_sdk import OnspringClient

        sync = OnspringClient(os.environ["API_BASE_URL"], os.environ["SANDBOX_API_KEY"])

        record_id = self._create_temp_record(sync, test_survey_id, test_text_field)

        response = await async_client.delete_record_by_id(app_id=test_survey_id, record_id=record_id)

        assert response.status_code == 204
        assert response.is_successful

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        response = bad.delete_record_by_id(app_id=1, record_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        response = client.delete_record_by_id(app_id=test_app_id_no_access, record_id=1)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_record_not_found_returns_404(self, client, test_app_id):
        response = client.delete_record_by_id(app_id=test_app_id, record_id=0)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestDeleteRecordsByIds:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id, test_text_field):
        r1 = client.add_or_update_record(
            Record(app_id=test_survey_id, fields=[StringFieldValue(field_id=test_text_field, value="del1")])
        )

        r2 = client.add_or_update_record(
            Record(app_id=test_survey_id, fields=[StringFieldValue(field_id=test_text_field, value="del2")])
        )

        assert r1.data is not None and r2.data is not None

        request = DeleteBatchRecordsRequest(app_id=test_survey_id, record_ids=[r1.data.id, r2.data.id])

        response = client.delete_records_by_ids(request)

        assert response.status_code == 204
        assert response.is_successful

    @pytest.mark.flaky(reruns=3)
    def test_empty_ids_returns_400(self, client, test_survey_id):
        request = DeleteBatchRecordsRequest(app_id=test_survey_id, record_ids=[])

        response = client.delete_records_by_ids(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = DeleteBatchRecordsRequest(app_id=1, record_ids=[1])

        response = bad.delete_records_by_ids(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        request = DeleteBatchRecordsRequest(app_id=test_app_id_no_access, record_ids=[1])

        response = client.delete_records_by_ids(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None


class TestGetRecordsByIds:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id, test_survey_record_id):
        request = GetBatchRecordsRequest(app_id=test_survey_id, record_ids=[test_survey_record_id])

        response = client.get_records_by_ids(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.count is not None
        assert len(response.data.records) > 0

        for record in response.data.records:
            assert record.app_id == test_survey_id
            assert record.record_id is not None
            assert record.fields is not None
            assert len(record.fields) > 0

            for field in record.fields:
                assert field.field_id is not None
                assert field.type is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id, test_survey_record_id):
        request = GetBatchRecordsRequest(app_id=test_survey_id, record_ids=[test_survey_record_id])

        response = await async_client.get_records_by_ids(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.records) > 0

    @pytest.mark.flaky(reruns=3)
    def test_with_params(self, client, test_survey_id, test_survey_record_id, test_text_field):
        request = GetBatchRecordsRequest(
            app_id=test_survey_id,
            record_ids=[test_survey_record_id],
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
        )

        response = client.get_records_by_ids(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.records) > 0

    @pytest.mark.flaky(reruns=3)
    async def test_with_params_async(self, async_client, test_survey_id, test_survey_record_id, test_text_field):
        request = GetBatchRecordsRequest(
            app_id=test_survey_id,
            record_ids=[test_survey_record_id],
            field_ids=[test_text_field],
            data_format=DataFormat.Formatted.name,
        )

        response = await async_client.get_records_by_ids(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_too_many_ids_returns_400(self, client):
        record_ids = list(range(1, 102))
        request = GetBatchRecordsRequest(app_id=1, record_ids=record_ids)

        response = client.get_records_by_ids(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_too_many_ids_returns_400_async(self, async_client):
        record_ids = list(range(1, 102))
        request = GetBatchRecordsRequest(app_id=1, record_ids=record_ids)

        response = await async_client.get_records_by_ids(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = GetBatchRecordsRequest(app_id=1, record_ids=[1])

        response = bad.get_records_by_ids(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        request = GetBatchRecordsRequest(app_id=1, record_ids=[1])

        response = await bad.get_records_by_ids(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        request = GetBatchRecordsRequest(app_id=test_app_id_no_access, record_ids=[1])

        response = client.get_records_by_ids(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access):
        request = GetBatchRecordsRequest(app_id=test_app_id_no_access, record_ids=[1])

        response = await async_client.get_records_by_ids(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None


class TestQueryRecords:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(app_id=test_survey_id, filter=filter_str)

        response = client.query_records(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.page_number is not None
        assert response.data.page_size is not None
        assert response.data.total_pages is not None
        assert response.data.total_records is not None

        for record in response.data.records:
            assert record.app_id == test_survey_id
            assert record.record_id is not None
            assert record.fields is not None

            if record.fields:
                for field in record.fields:
                    assert field.field_id is not None
                    assert field.type is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(app_id=test_survey_id, filter=filter_str)

        response = await async_client.query_records(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.total_records is not None

    @pytest.mark.flaky(reruns=3)
    def test_with_params(self, client, test_survey_id, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(
            app_id=test_survey_id,
            filter=filter_str,
            field_ids=[test_survey_auto_number_field],
            data_format=DataFormat.Formatted.name,
            page_number=1,
            page_size=1,
        )

        response = client.query_records(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1

    @pytest.mark.flaky(reruns=3)
    async def test_with_params_async(self, async_client, test_survey_id, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(
            app_id=test_survey_id,
            filter=filter_str,
            field_ids=[test_survey_auto_number_field],
            data_format=DataFormat.Formatted.name,
            page_number=1,
            page_size=1,
        )

        response = await async_client.query_records(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.page_number == 1
        assert response.data.page_size == 1

    @pytest.mark.flaky(reruns=3)
    def test_invalid_page_size_returns_400(self, client, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(
            app_id=1,
            filter=filter_str,
            page_size=-1,
        )

        response = client.query_records(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_page_size_returns_400_async(self, async_client, test_survey_auto_number_field):
        filter_str = f"{test_survey_auto_number_field} gt 0"
        request = QueryRecordsRequest(
            app_id=1,
            filter=filter_str,
            page_size=-1,
        )

        response = await async_client.query_records(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = QueryRecordsRequest(app_id=1, filter="")

        response = bad.query_records(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        request = QueryRecordsRequest(app_id=1, filter="")

        response = await bad.query_records(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access, test_text_field):
        filter_str = f"{test_text_field} gt ''"
        request = QueryRecordsRequest(app_id=test_app_id_no_access, filter=filter_str)

        response = client.query_records(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access, test_text_field):
        filter_str = f"{test_text_field} gt ''"
        request = QueryRecordsRequest(app_id=test_app_id_no_access, filter=filter_str)

        response = await async_client.query_records(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None
