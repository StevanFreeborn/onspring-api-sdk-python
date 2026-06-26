import os

import pytest

from onspring_api_sdk import OnspringClient
from onspring_api_sdk.models import Record, StringFieldValue


def add_record(base_url: str, api_key: str) -> int:
    client = OnspringClient(base_url, api_key)

    survey_id = os.environ.get("TEST_SURVEY_ID")
    text_field = os.environ.get("TEST_TEXT_FIELD")

    if survey_id is None:
        pytest.fail("TEST_SURVEY_ID is not defined")
    if text_field is None:
        pytest.fail("TEST_TEXT_FIELD is not defined")

    app_id = int(survey_id)
    field_id = int(text_field)

    record = Record(
        app_id=app_id,
        fields=[StringFieldValue(field_id=field_id, value="test")],
    )

    response = client.add_or_update_record(record)

    if response.data is None or response.data.id is None:
        pytest.fail("Record ID is not defined")

    return response.data.id
