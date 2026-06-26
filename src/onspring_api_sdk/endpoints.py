"""URL builder functions for all Onspring API v2 endpoints."""


def get_ping_endpoint(base_url: str) -> str:
    """Build the ping endpoint URL."""
    return f"{base_url}/Ping"


def get_apps_endpoint(base_url: str) -> str:
    """Build the get-apps endpoint URL."""
    return f"{base_url}/Apps"


def get_app_by_id_endpoint(base_url: str, app_id: int) -> str:
    """Build the get-app-by-id endpoint URL."""
    return f"{base_url}/Apps/id/{app_id}"


def get_apps_by_ids_endpoint(base_url: str) -> str:
    """Build the get-apps-by-ids endpoint URL."""
    return f"{base_url}/Apps/batch-get"


def get_field_by_id_endpoint(base_url: str, field_id: int) -> str:
    """Build the get-field-by-id endpoint URL."""
    return f"{base_url}/Fields/id/{field_id}"


def get_fields_by_ids_endpoint(base_url: str) -> str:
    """Build the get-fields-by-ids endpoint URL."""
    return f"{base_url}/Fields/batch-get"


def get_fields_by_app_id_endpoint(base_url: str, app_id: int) -> str:
    """Build the get-fields-by-app-id endpoint URL."""
    return f"{base_url}/Fields/appId/{app_id}"


def get_file_info_by_id_endpoint(base_url: str, record_id: int, field_id: int, file_id: int) -> str:
    """Build the get-file-info-by-id endpoint URL."""
    return f"{base_url}/Files/recordId/{record_id}/fieldId/{field_id}/fileId/{file_id}"


def delete_file_by_id_endpoint(base_url: str, record_id: int, field_id: int, file_id: int) -> str:
    """Build the delete-file-by-id endpoint URL."""
    return f"{base_url}/Files/recordId/{record_id}/fieldId/{field_id}/fileId/{file_id}"


def get_file_by_id_endpoint(base_url: str, record_id: int, field_id: int, file_id: int) -> str:
    """Build the get-file-by-id endpoint URL."""
    return f"{base_url}/Files/recordId/{record_id}/fieldId/{field_id}/fileId/{file_id}/file"


def save_file_endpoint(base_url: str) -> str:
    """Build the save-file endpoint URL."""
    return f"{base_url}/Files"


def add_or_update_list_item_endpoint(base_url: str, list_id: int) -> str:
    """Build the add-or-update-list-item endpoint URL."""
    return f"{base_url}/Lists/id/{list_id}/items"


def delete_list_item_endpoint(base_url: str, list_id: int, item_id: str) -> str:
    """Build the delete-list-item endpoint URL."""
    return f"{base_url}/Lists/id/{list_id}/itemId/{item_id}"


def get_records_by_app_id_endpoint(base_url: str, app_id: int) -> str:
    """Build the get-records-by-app-id endpoint URL."""
    return f"{base_url}/Records/appId/{app_id}"


def get_record_by_id_endpoint(base_url: str, app_id: int, record_id: int) -> str:
    """Build the get-record-by-id endpoint URL."""
    return f"{base_url}/Records/appId/{app_id}/recordId/{record_id}"


def delete_record_by_id_endpoint(base_url: str, app_id: int, record_id: int) -> str:
    """Build the delete-record-by-id endpoint URL."""
    return f"{base_url}/Records/appId/{app_id}/recordId/{record_id}"


def get_records_by_ids_endpoint(base_url: str) -> str:
    """Build the get-records-by-ids endpoint URL."""
    return f"{base_url}/Records/batch-get"


def query_records_endpoint(base_url: str) -> str:
    """Build the query-records endpoint URL."""
    return f"{base_url}/Records/Query"


def add_or_update_record_endpoint(base_url: str) -> str:
    """Build the add-or-update-record endpoint URL."""
    return f"{base_url}/Records"


def delete_records_by_ids_endpoint(base_url: str) -> str:
    """Build the delete-records-by-ids endpoint URL."""
    return f"{base_url}/Records/batch-delete"


def get_report_by_id_endpoint(base_url: str, report_id: int) -> str:
    """Build the get-report-by-id endpoint URL."""
    return f"{base_url}/Reports/id/{report_id}"


def get_reports_by_app_id_endpoint(base_url: str, app_id: int) -> str:
    """Build the get-reports-by-app-id endpoint URL."""
    return f"{base_url}/Reports/appId/{app_id}"
