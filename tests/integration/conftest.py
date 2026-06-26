import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from onspring_api_sdk import AsyncOnspringClient, OnspringClient

load_dotenv()


def _required_env(key: str) -> str:
    value = os.environ.get(key)
    if value is None:
        pytest.fail(f"{key} is not defined")
    return value


def _optional_env(key: str) -> str | None:
    return os.environ.get(key)


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marks tests as integration tests (real API calls)")


@pytest.fixture(scope="session")
def base_url():
    return _required_env("API_BASE_URL")


@pytest.fixture(scope="session")
def api_key():
    return _required_env("SANDBOX_API_KEY")


@pytest.fixture(scope="session")
def test_app_id():
    return int(_required_env("TEST_APP_ID"))


@pytest.fixture(scope="session")
def test_survey_id():
    return int(_required_env("TEST_SURVEY_ID"))


@pytest.fixture(scope="session")
def test_app_id_no_access():
    return int(_required_env("TEST_APP_ID_NO_ACCESS"))


@pytest.fixture(scope="session")
def test_app_ids():
    raw = _required_env("TEST_APP_IDS")
    return [int(x) for x in raw.split(",")]


@pytest.fixture(scope="session")
def test_app_ids_no_access():
    raw = _required_env("TEST_APP_IDS_NO_ACCESS")
    return [int(x) for x in raw.split(",")]


@pytest.fixture(scope="session")
def test_field_id():
    return int(_required_env("TEST_FIELD_ID"))


@pytest.fixture(scope="session")
def test_field_id_no_access():
    return int(_required_env("TEST_FIELD_ID_NO_ACCESS"))


@pytest.fixture(scope="session")
def test_field_ids():
    raw = _required_env("TEST_FIELD_IDS")
    return [int(x) for x in raw.split(",")]


@pytest.fixture(scope="session")
def test_field_ids_no_access():
    raw = _required_env("TEST_FIELD_IDS_NO_ACCESS")
    return [int(x) for x in raw.split(",")]


@pytest.fixture(scope="session")
def test_record():
    return int(_required_env("TEST_RECORD"))


@pytest.fixture(scope="session")
def test_survey_record_id():
    return int(_required_env("TEST_SURVEY_RECORD_ID"))


@pytest.fixture(scope="session")
def test_text_field():
    return int(_required_env("TEST_TEXT_FIELD"))


@pytest.fixture(scope="session")
def test_attachment_field():
    return int(_required_env("TEST_ATTACHMENT_FIELD"))


@pytest.fixture(scope="session")
def test_attachment_field_no_access_field():
    return int(_required_env("TEST_ATTACHMENT_FIELD_NO_ACCESS_FIELD"))


@pytest.fixture(scope="session")
def test_attachment_field_no_access_app():
    return int(_required_env("TEST_ATTACHMENT_FIELD_NO_ACCESS_APP"))


@pytest.fixture(scope="session")
def test_attachment():
    return int(_required_env("TEST_ATTACHMENT"))


@pytest.fixture(scope="session")
def test_image_field():
    return int(_required_env("TEST_IMAGE_FIELD"))


@pytest.fixture(scope="session")
def test_image():
    return int(_required_env("TEST_IMAGE"))


@pytest.fixture(scope="session")
def test_list_field():
    return int(_required_env("TEST_LIST_FIELD"))


@pytest.fixture(scope="session")
def test_list_field_no_access():
    return int(_required_env("TEST_LIST_FIELD_NO_ACCESS"))


@pytest.fixture(scope="session")
def test_list_id():
    return int(_required_env("TEST_LIST_ID"))


@pytest.fixture(scope="session")
def test_list_id_no_access():
    return int(_required_env("TEST_LIST_ID_NO_ACCESS"))


@pytest.fixture(scope="session")
def test_list_item_id_no_access():
    return _required_env("TEST_LIST_ITEM_ID_NO_ACCESS")


@pytest.fixture(scope="session")
def test_report():
    return int(_required_env("TEST_REPORT"))


@pytest.fixture(scope="session")
def test_report_no_access():
    return int(_required_env("TEST_REPORT_NO_ACCESS"))


@pytest.fixture(scope="session")
def test_report_with_chart_data():
    return int(_required_env("TEST_REPORT_WITH_CHART_DATA"))


@pytest.fixture(scope="session")
def test_survey_auto_number_field():
    return _optional_env("TEST_SURVEY_AUTO_NUMBER_FIELD")


@pytest.fixture(scope="session")
def testdata_dir():
    return Path(__file__).parent / "testdata"


@pytest.fixture
def client(base_url, api_key):
    return OnspringClient(base_url, api_key)


@pytest.fixture
def async_client(base_url, api_key):
    return AsyncOnspringClient(base_url, api_key)
