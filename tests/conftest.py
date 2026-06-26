from pathlib import Path

import pytest

from onspring_api_sdk import AsyncOnspringClient, OnspringClient

TEST_URL = "https://test.com"
TEST_API_KEY = "apiKey"


@pytest.fixture
def client():
    return OnspringClient(TEST_URL, TEST_API_KEY)


@pytest.fixture
def async_client():
    return AsyncOnspringClient(TEST_URL, TEST_API_KEY)


MOCK_APP = {
    "href": "https://api.onspring.com/Apps/id/1",
    "id": 1,
    "name": "Test App",
}

MOCK_APPS_RESPONSE = {
    "pageNumber": 1,
    "pageSize": 50,
    "totalPages": 1,
    "totalRecords": 2,
    "items": [
        MOCK_APP,
        {**MOCK_APP, "id": 2, "name": "App 2"},
    ],
}

MOCK_APPS_BATCH_RESPONSE = {
    "count": 2,
    "items": [MOCK_APP, {**MOCK_APP, "id": 2, "name": "App 2"}],
}


MOCK_FIELD = {
    "id": 1,
    "appId": 10,
    "name": "Test Field",
    "type": "Text",
    "status": "Enabled",
    "isRequired": True,
    "isUnique": False,
}

MOCK_LIST_FIELD = {
    "id": 2,
    "appId": 10,
    "name": "List Field",
    "type": "List",
    "status": "Enabled",
    "isRequired": False,
    "isUnique": False,
    "multiplicity": "SingleSelect",
    "listId": 100,
    "values": [
        {
            "id": "2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84",
            "name": "list_value_1",
            "sortOrder": 1,
            "numericValue": 1,
            "color": "#008e8e",
        },
    ],
}

MOCK_FIELDS_RESPONSE = {
    "pageNumber": 1,
    "pageSize": 50,
    "totalPages": 1,
    "totalRecords": 2,
    "items": [MOCK_FIELD, MOCK_LIST_FIELD],
}

MOCK_FIELDS_BATCH_RESPONSE = {
    "count": 2,
    "items": [MOCK_FIELD, MOCK_LIST_FIELD],
}


MOCK_FILE_INFO = {
    "type": "Attachment",
    "contentType": "text/plain",
    "name": "test.txt",
    "createdDate": "2024-01-01T00:00:00",
    "modifiedDate": "2024-01-01T00:00:00",
    "owner": "Test User",
    "notes": "Test note",
    "fileHref": "https://api.onspring.com/Files/...",
}

MOCK_SAVE_FILE_RESPONSE = {"id": 1}


MOCK_LIST_ITEM_RESPONSE = {"id": "00000000-0000-0000-0000-000000000000"}


MOCK_RECORD = {
    "appId": 100,
    "recordId": 1,
    "fieldData": [
        {"fieldId": 1, "value": "Test Value", "type": "String"},
        {"fieldId": 2, "value": 42, "type": "Integer"},
    ],
}

MOCK_RECORDS_RESPONSE = {
    "pageNumber": 1,
    "pageSize": 50,
    "totalPages": 1,
    "totalRecords": 1,
    "items": [MOCK_RECORD],
}

MOCK_RECORDS_BATCH_RESPONSE = {
    "count": 1,
    "items": [MOCK_RECORD],
}

MOCK_SAVE_RECORD_RESPONSE = {
    "id": 1,
    "warnings": [],
}


MOCK_REPORT_RESPONSE = {
    "columns": ["col1", "col2"],
    "rows": [
        {"recordId": 1, "cells": ["a", "b"]},
    ],
}

MOCK_REPORT_BY_APP = {
    "appId": 10,
    "id": 53,
    "name": "Test Report",
    "description": "A test report",
}

MOCK_REPORTS_BY_APP_RESPONSE = {
    "pageNumber": 1,
    "pageSize": 50,
    "totalPages": 1,
    "totalRecords": 1,
    "items": [MOCK_REPORT_BY_APP],
}


MOCK_MESSAGE_RESPONSE = {"message": "An error occurred"}


TEMP_DIR = Path(__file__).parent / "_temp"


@pytest.fixture(autouse=True)
def manage_temp_dir():
    TEMP_DIR.mkdir(exist_ok=True)
    yield
    if TEMP_DIR.exists():
        for f in TEMP_DIR.iterdir():
            f.unlink()
        TEMP_DIR.rmdir()


def create_temp_file(name: str = "test.txt", content: bytes = b"Hello World!") -> Path:
    path = TEMP_DIR / name
    path.write_bytes(content)
    return path
