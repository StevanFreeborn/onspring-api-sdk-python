import pytest

from onspring_api_sdk.enums import ReportDataType
from onspring_api_sdk.models import GetReportByIdRequest, PagingRequest

pytestmark = pytest.mark.integration


class TestGetReportById:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_report):
        request = GetReportByIdRequest(report_id=test_report)

        response = client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.columns is not None
        assert len(response.data.columns) > 0
        assert response.data.rows is not None
        assert len(response.data.rows) > 0

        for row in response.data.rows:
            assert row.record_id is not None
            assert row.cells is not None
            assert len(row.cells) > 0

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_report):
        request = GetReportByIdRequest(report_id=test_report)

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.rows) > 0

    @pytest.mark.flaky(reruns=3)
    def test_with_chart_data_report(self, client, test_report_with_chart_data):
        request = GetReportByIdRequest(report_id=test_report_with_chart_data)

        response = client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.columns is not None
        assert response.data.rows is not None

    @pytest.mark.flaky(reruns=3)
    async def test_with_chart_data_report_async(self, async_client, test_report_with_chart_data):
        request = GetReportByIdRequest(report_id=test_report_with_chart_data)

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_request_chart_data(self, client, test_report_with_chart_data):
        request = GetReportByIdRequest(
            report_id=test_report_with_chart_data,
            data_type=ReportDataType.ChartData.name,
        )

        response = client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert response.data.columns is not None
        assert response.data.rows is not None

    @pytest.mark.flaky(reruns=3)
    async def test_request_chart_data_async(self, async_client, test_report_with_chart_data):
        request = GetReportByIdRequest(
            report_id=test_report_with_chart_data,
            data_type=ReportDataType.ChartData.name,
        )

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None

    @pytest.mark.flaky(reruns=3)
    def test_chart_data_on_report_without_returns_400(self, client, test_report):
        request = GetReportByIdRequest(
            report_id=test_report,
            data_type=ReportDataType.ChartData.name,
        )

        response = client.get_report_by_id(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_chart_data_on_report_without_returns_400_async(self, async_client, test_report):
        request = GetReportByIdRequest(
            report_id=test_report,
            data_type=ReportDataType.ChartData.name,
        )

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 400
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_invalid_api_key_returns_401(self, base_url):
        from onspring_api_sdk import OnspringClient

        bad = OnspringClient(base_url, "invalid")
        request = GetReportByIdRequest(report_id=1)

        response = bad.get_report_by_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        request = GetReportByIdRequest(report_id=1)

        response = await bad.get_report_by_id(request)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client):
        request = GetReportByIdRequest(report_id=1)

        response = client.get_report_by_id(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client):
        request = GetReportByIdRequest(report_id=1)

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_not_found_returns_404(self, client):
        request = GetReportByIdRequest(report_id=0)

        response = client.get_report_by_id(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_not_found_returns_404_async(self, async_client):
        request = GetReportByIdRequest(report_id=0)

        response = await async_client.get_report_by_id(request)

        assert response.status_code == 404
        assert not response.is_successful
        assert response.data is None


class TestGetReportsByAppId:
    @pytest.mark.flaky(reruns=3)
    def test_sync(self, client, test_survey_id):
        response = client.get_reports_by_app_id(app_id=test_survey_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.message is None
        assert response.data is not None
        assert response.data.page_number is not None
        assert response.data.page_size is not None
        assert response.data.total_pages is not None
        assert response.data.total_records is not None
        assert response.data.reports is not None
        assert len(response.data.reports) > 0

        for report in response.data.reports:
            assert report.app_id is not None
            assert report.id is not None
            assert report.name is not None

    @pytest.mark.flaky(reruns=3)
    async def test_async(self, async_client, test_survey_id):
        response = await async_client.get_reports_by_app_id(app_id=test_survey_id)

        assert response.status_code == 200
        assert response.is_successful
        assert response.data is not None
        assert len(response.data.reports) > 0

    @pytest.mark.flaky(reruns=3)
    def test_invalid_page_size_returns_400(self, client, test_survey_id):
        response = client.get_reports_by_app_id(
            app_id=test_survey_id,
            paging_request=PagingRequest(page_number=1, page_size=-1),
        )

        assert response.status_code == 400
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_page_size_returns_400_async(self, async_client, test_survey_id):
        response = await async_client.get_reports_by_app_id(
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
        response = bad.get_reports_by_app_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_invalid_api_key_returns_401_async(self, base_url):
        from onspring_api_sdk import AsyncOnspringClient

        bad = AsyncOnspringClient(base_url, "invalid")
        response = await bad.get_reports_by_app_id(app_id=1)

        assert response.status_code == 401
        assert not response.is_successful
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    def test_no_access_returns_403(self, client, test_app_id_no_access):
        response = client.get_reports_by_app_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.message is not None
        assert response.data is None

    @pytest.mark.flaky(reruns=3)
    async def test_no_access_returns_403_async(self, async_client, test_app_id_no_access):
        response = await async_client.get_reports_by_app_id(app_id=test_app_id_no_access)

        assert response.status_code == 403
        assert not response.is_successful
        assert response.data is None
