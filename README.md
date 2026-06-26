# Onspring API Python SDK

The python SDK for **version 2** of the Onspring API is meant to simplify development in Python for Onspring customers who want to build integrations with their Onspring instance.

**Note:**
This is an unofficial SDK for the Onspring API. It was not built in consultation with Onspring Technologies LLC or a member of their development team.

This SDK was developed independently using their existing C# SDK, their swagger page, and api documentation as the starting point with the intention of making development of integrations done in Python with an Onspring instance quicker and more convenient.

## Dependencies

### Python

Requires use of Python 3.10.0 or later.

### httpx

All methods for `OnspringClient` and `AsyncOnspringClient` make use of the [httpx](https://www.python-httpx.org/) library to interact with the endpoints of version 2 of the Onspring API.

## Installation

Install the SDK using pip:

`pip install OnspringApiSdk`

## API Key

In order to successfully interact with the Onspring Api you will need an API key. API keys are obtained by an Onspring user with permissions to at least **Read** API Keys for your instance via the following steps:

1. Login to the Onspring instance.
2. Navigate to **Administration** > **Security** > **API Keys**
3. On the list page, add a new API Key - this will require **Create** permissions - or click an existing API key to view its details.
4. Click on the **Developer Information** tab.
5. Copy the **X-ApiKey Header** value from this tab.

## Start Coding

### `OnspringClient`

The most common way to use the SDK is to create an `OnspringClient` instance and call its methods. Its constructor requires two parameters:

- `url` - currently this should always be: `https://api.onspring.com`
- `key` - the value obtained by following the steps in the **API Key** section

It is best practice to read these values in from a configuration file for both flexibility and security purposes.

Example `config.ini` file:

```ini
[prod]
key = 000000ffffff000000ffffff/00000000-ffff-0000-ffff-000000000000
url = https://api.onspring.com
```

Example constructing `OnspringClient`:

```python
from onspring_api_sdk import OnspringClient
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

client = OnspringClient(url, key)
```

### `AsyncOnspringClient`

An async client is also available for use with `asyncio`:

```python
from onspring_api_sdk import AsyncOnspringClient

async with AsyncOnspringClient(url, key) as client:
    response = await client.get_apps()
```

All methods mirror the sync client with `await` prefixed.

### `ApiResponse`

Each client method returns an `ApiResponse` object with the following properties:

- `status_code` - The http status code of the response.
- `is_successful` - Whether the request was successful (status < 400).
- `data` - If the request was successful will contain the response data deserialized to Pydantic models.
- `message` - A message that may provide more detail about the requests success or failure.
- `raw_response` - Exposes the raw [`httpx.Response`](https://www.python-httpx.org/api/#response) object if you'd like to handle it directly.

The goal with this `ApiResponse` object is to provide the flexibility to do with the response what you'd like while already having the JSON response deserialized to Python objects.

### Error Handling

You can check `is_successful` or call `raise_for_status()` to raise an exception on failure:

```python
from onspring_api_sdk import OnspringError, OnspringAuthenticationError

response = client.get_apps()

if not response.is_successful:
    print(f'Request failed: {response.message}')

# Or raise on failure:
try:
    response.raise_for_status()
except OnspringAuthenticationError:
    print('Check your API key')
except OnspringError as e:
    print(f'Request failed: {e}')
```

## Full API Documentation

You may wish to refer to the full [Onspring API documentation](https://software.onspring.com/hubfs/Training/Admin%20Guide%20-%20v2%20API.pdf) when determining which values to pass as parameters to some of the client methods. There is also a [swagger page](https://api.onspring.com/swagger/index.html) that you can use for making exploratory requests.

## Example Code

The examples that follow assume you have created an `OnspringClient` as described in the **Start Coding** section.

### Connectivity

#### Verify connectivity

```python
if client.can_connect():
    print('Connected successfully')
else:
    print('Attempt to connect failed')
```

### Apps

#### Get Apps

Returns a paged collection of apps and/or surveys that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.get_apps()

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

You can set your own page size and page number (max is 1,000) as well.

```python
from onspring_api_sdk.models import PagingRequest

paging_request = PagingRequest(page_number=1, page_size=100)
response = client.get_apps(paging_request=paging_request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

#### Get App By Id

Returns an Onspring app or survey according to provided id.

```python
response = client.get_app_by_id(app_id=195)

print(f'Status Code: {response.status_code}')
print(f'id: {response.data.app.id}')
print(f'Name: {response.data.app.name}')
print(f'href: {response.data.app.href}')
```

#### Get Apps By Ids

Returns a collection of Onspring apps and/or surveys according to provided ids.

```python
response = client.get_apps_by_ids(app_ids=[195, 240])

print(f'Status Code: {response.status_code}')
print(f'Count: {response.data.count}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

### Fields

#### Print Field Helper

An example helper for printing field details used in the following examples:

```python
from onspring_api_sdk.models import OnspringField


def print_field(field: OnspringField):

    print('Field:')
    print(f' Id: {field.id}')
    print(f' App Id: {field.app_id}')
    print(f' Name: {field.name}')
    print(f' Type: {field.type}')
    print(f' Status: {field.status}')
    print(f' Is Required: {field.is_required}')
    print(f' Is Unique: {field.is_unique}')

    if field.type == 'Formula':
        print(f' Output Type: {field.output_type}')

    if field.type == 'List':
        print(f' Multiplicity: {field.multiplicity}')

        if field.values:
            print(' Values:')

            for value in field.values:
                print(f'  {value}')
```

#### Get Field By Id

Returns an Onspring field according to provided id.

```python
response = client.get_field_by_id(field_id=9686)

print(f'Status Code: {response.status_code}')
print_field(response.data.field)
```

#### Get Fields By Ids

Returns a collection of Onspring fields according to provided ids.

```python
response = client.get_fields_by_ids(field_ids=[9686, 9687])

print(f'Status Code: {response.status_code}')
print(f'Count: {response.data.count}')

for field in response.data.fields:
    print_field(field)
```

#### Get Fields By App Id

Returns a paged collection of fields that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.get_fields_by_app_id(app_id=195)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for field in response.data.fields:
    print_field(field)
```

You can set your own page size and page number (max is 1,000) as well.

```python
from onspring_api_sdk.models import PagingRequest

paging_request = PagingRequest(page_number=1, page_size=100)
response = client.get_fields_by_app_id(app_id=195, paging_request=paging_request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for field in response.data.fields:
    print_field(field)
```

### Files

#### Get File Info By Id

Returns the Onspring file's metadata.

```python
response = client.get_file_info_by_id(record_id=1, field_id=6990, file_id=274)

print(f'Status Code: {response.status_code}')
print(f'Name: {response.data.file_info.name}')
print(f'Type: {response.data.file_info.type}')
print(f'Owner: {response.data.file_info.owner}')
print(f'Content Type: {response.data.file_info.content_type}')
print(f'Created Date: {response.data.file_info.created_date}')
print(f'Modified Date: {response.data.file_info.modified_date}')
print(f'File Href: {response.data.file_info.file_href}')
```

#### Get File By Id

Returns the file itself.

```python
response = client.get_file_by_id(record_id=1, field_id=6990, file_id=274)

print(f'Status Code: {response.status_code}')
print(f'Name: {response.data.file.name}')
print(f'Content Type: {response.data.file.content_type}')
print(f'Content Length: {response.data.file.content_length}')

file_path = f'C:\\Users\\sfree\\Documents\\Temp\\{response.data.file.name}'

with open(file_path, "wb") as f:
    f.write(response.data.file.content)

print(f'File Location: {file_path}')
```

#### Save File

```python
from onspring_api_sdk.models import SaveFileRequest
from datetime import datetime
import os
import mimetypes

file_path = 'C:\\Users\\sfree\\Documents\\Temp\\Test Attachment.txt'
file_name = os.path.basename(file_path)
content_type = mimetypes.guess_type(file_path)[0]

request = SaveFileRequest(
    record_id=60,
    field_id=6989,
    file_name=file_name,
    file_path=file_path,
    content_type=content_type,
    notes='Initial revision',
    modified_date=datetime.now(),
)

response = client.save_file(request)

print(f'Status Code: {response.status_code}')
print(f'File Id: {response.data.id}')
```

#### Delete File By Id

```python
response = client.delete_file_by_id(record_id=60, field_id=6989, file_id=231)

print(f'Status Code: {response.status_code}')
print(f'Message: {response.message}')
```

### Lists

#### Add Or Update List Value

To add a list value don't provide an id value.

```python
from onspring_api_sdk.models import ListItemRequest

request = ListItemRequest(
    list_id=906,
    name='Not Started',
    numeric_value=0,
    color='#ffffff',
)

response = client.add_or_update_list_item(request)

print(f'Status Code: {response.status_code}')
print(f'Id: {response.data.id}')
```

To update a list value provide an id value.

```python
from onspring_api_sdk.models import ListItemRequest
import uuid

request = ListItemRequest(
    list_id=906,
    name='Pending',
    id=uuid.UUID('4118d53a-9121-4345-8682-07f23d606daa'),
    numeric_value=0,
    color='#ffffff',
)

response = client.add_or_update_list_item(request)

print(f'Status Code: {response.status_code}')
print(f'Id: {response.data.id}')
```

#### Delete List Value

```python
response = client.delete_list_item(
    list_id=906,
    item_id='36f94d8c-2b9d-465e-9ad1-ede04109efc9',
)

print(f'Status Code: {response.status_code}')
print(f'Message: {response.message}')
```

### Records

#### Get Records By App Id

Returns a paged collection of records that can be paged through. By default the page size is 50 and page number is 1.

```python
from onspring_api_sdk.models import GetRecordsByAppRequest

request = GetRecordsByAppRequest(app_id=195)
response = client.get_records_by_app_id(request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

You can set your own page size and page number (max is 1,000) as well. In addition to specifying what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from onspring_api_sdk.models import GetRecordsByAppRequest
from onspring_api_sdk.enums import DataFormat

request = GetRecordsByAppRequest(
    app_id=195,
    field_ids=[9686],
    data_format=DataFormat.Formatted.name,
    page_number=1,
    page_size=10,
)

response = client.get_records_by_app_id(request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

#### Get Record By Id

Returns an Onspring record based on the provided app and record ids.

```python
from onspring_api_sdk.models import GetRecordByIdRequest

request = GetRecordByIdRequest(app_id=195, record_id=60)
response = client.get_record_by_id(request)

print(f'Status Code: {response.status_code}')
print(f'AppId: {response.data.app_id}')
print(f'RecordId: {response.data.record_id}')

for field in response.data.fields:
    print(f'Type: {field.type}')
    print(f'FieldId: {field.field_id}')
    print(f'Value: {field.value}')
```

You can also specify what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from onspring_api_sdk.models import GetRecordByIdRequest
from onspring_api_sdk.enums import DataFormat

request = GetRecordByIdRequest(
    app_id=195,
    record_id=60,
    field_ids=[9686],
    data_format=DataFormat.Formatted.name,
)

response = client.get_record_by_id(request)

print(f'Status Code: {response.status_code}')
print(f'AppId: {response.data.app_id}')
print(f'RecordId: {response.data.record_id}')

for field in response.data.fields:
    print(f'Type: {field.type}')
    print(f'FieldId: {field.field_id}')
    print(f'Value: {field.value}')
```

#### Delete Record By Id

```python
response = client.delete_record_by_id(app_id=195, record_id=60)

print(f'Status Code: {response.status_code}')
print(f'Message: {response.message}')
```

#### Get Records By Ids

Returns a collection of Onspring records based on the provided appId and recordIds.

```python
from onspring_api_sdk.models import GetBatchRecordsRequest

request = GetBatchRecordsRequest(app_id=195, record_ids=[1, 2, 3])
response = client.get_records_by_ids(request)

print(f'Status Code: {response.status_code}')
print(f'Count: {response.data.count}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

You can also specify what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from onspring_api_sdk.models import GetBatchRecordsRequest
from onspring_api_sdk.enums import DataFormat

request = GetBatchRecordsRequest(
    app_id=195,
    record_ids=[1, 2, 3],
    field_ids=[9686],
    data_format=DataFormat.Formatted.name,
)

response = client.get_records_by_ids(request)

print(f'Status Code: {response.status_code}')
print(f'Count: {response.data.count}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

#### Query Records

Returns a paged collection of records based on a criteria that can be paged through. By default the page size is 50 and page number is 1.

```python
from onspring_api_sdk.models import QueryRecordsRequest

field_id = 6983
operator = 'eq'
value = "'Test Task 5'"

request = QueryRecordsRequest(app_id=195, filter=f'{field_id} {operator} {value}')
response = client.query_records(request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

You can set your own page size and page number (max is 1,000) as well. In addition to specifying what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from onspring_api_sdk.models import QueryRecordsRequest
from onspring_api_sdk.enums import DataFormat

field_id = 6983
operator = 'eq'
value = "'Test Task 5'"

request = QueryRecordsRequest(
    app_id=195,
    filter=f'{field_id} {operator} {value}',
    field_ids=[9686],
    data_format=DataFormat.Formatted.name,
    page_number=1,
    page_size=10,
)

response = client.query_records(request)

print(f'Status Code: {response.status_code}')
print(f'Page Size: {response.data.page_size}')
print(f'Page Number: {response.data.page_number}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')

for record in response.data.records:
    print(f'AppId: {record.app_id}')
    print(f'RecordId: {record.record_id}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.field_id}')
        print(f'Value: {field.value}')
```

For further details on constructing the `filter` parameter please refer to the [documentation](https://software.onspring.com/hubfs/Training/Admin%20Guide%20-%20v2%20API.pdf) for v2 of the Onspring API.

#### Add or Update A Record

You can add a record by not providing a record id value. If successful will return the id of the added record.

```python
from onspring_api_sdk.models import (
    StringFieldValue,
    GuidFieldValue,
    DateFieldValue,
    IntegerListValue,
    Record,
)
import uuid
from datetime import datetime

fields = []

status = uuid.UUID('4118d53a-9121-4345-8682-07f23d606daa')
due_date = datetime.utcnow()

fields.append(StringFieldValue(field_id=6983, value='Test Task via API'))
fields.append(StringFieldValue(field_id=6984, value='This is a task.'))
fields.append(GuidFieldValue(field_id=6986, value=status))
fields.append(DateFieldValue(field_id=6985, value=due_date))
fields.append(IntegerListValue(field_id=6987, value=[4]))

record = Record(app_id=195, fields=fields)

response = client.add_or_update_record(record)

print(f'Status Code: {response.status_code}')
print(f'Id: {response.data.id}')

for warning in response.data.warnings:
    print(f'Warning: {warning}')
```

You can update a record by providing its id. If successful will return the id of record updated.

```python
from onspring_api_sdk.models import (
    StringFieldValue,
    GuidFieldValue,
    DateFieldValue,
    IntegerListValue,
    Record,
)
import uuid
from datetime import datetime

fields = []

status = uuid.UUID('1c1c5f7e-cd03-4b70-9790-0f83b24b5863')
due_date = datetime.utcnow()

fields.append(StringFieldValue(field_id=6983, value='Test Task via API'))
fields.append(StringFieldValue(field_id=6984, value='This is a task.'))
fields.append(GuidFieldValue(field_id=6986, value=status))
fields.append(DateFieldValue(field_id=6985, value=due_date))
fields.append(IntegerListValue(field_id=6987, value=[4]))

record = Record(app_id=195, fields=fields, record_id=103)

response = client.add_or_update_record(record)

print(f'Status Code: {response.status_code}')
print(f'Id: {response.data.id}')

for warning in response.data.warnings:
    print(f'Warning: {warning}')
```

#### Delete Records By Ids

```python
from onspring_api_sdk.models import DeleteBatchRecordsRequest

request = DeleteBatchRecordsRequest(app_id=195, record_ids=[1, 2, 3])

response = client.delete_records_by_ids(request)

print(f'Status Code: {response.status_code}')
print(f'Message: {response.message}')
```

### Reports

#### Get Report By Id

Returns the report for the provided id.

```python
from onspring_api_sdk.models import GetReportByIdRequest

request = GetReportByIdRequest(report_id=53)
response = client.get_report_by_id(request)

print(f'Status Code: {response.status_code}')
print('Columns:')
print(f'{", ".join(response.data.columns)}')
print('Rows:')

for row in response.data.rows:
    cells = ', '.join([str(cell) for cell in row.cells])
    print(f'Record Id {row.record_id}: {cells}')
```

You can also specify the format of the data in the report as well as whether you are requesting the report's data or its chart data.

```python
from onspring_api_sdk.models import GetReportByIdRequest
from onspring_api_sdk.enums import DataFormat, ReportDataType

request = GetReportByIdRequest(
    report_id=53,
    api_data_format=DataFormat.Formatted.name,
    data_type=ReportDataType.ChartData.name,
)

response = client.get_report_by_id(request)

print(f'Status Code: {response.status_code}')
print('Columns:')
print(f'{", ".join(response.data.columns)}')
print('Rows:')

for row in response.data.rows:
    cells = ', '.join([str(cell) for cell in row.cells])
    print(f'Record Id {row.record_id}: {cells}')
```

#### Get Reports By App Id

Returns a paged collection of reports that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.get_reports_by_app_id(app_id=195)

print(f'Status Code: {response.status_code}')
print('Reports:')

for report in response.data.reports:
    print(f' Id: {report.id}')
    print(f' Name: {report.name}')
    print(f' Description: {report.description}')
```

You can set your own page size and page number (max is 1,000) as well.

```python
from onspring_api_sdk.models import PagingRequest

paging_request = PagingRequest(page_number=1, page_size=10)
response = client.get_reports_by_app_id(app_id=195, paging_request=paging_request)

print(f'Status Code: {response.status_code}')
print(f'Page Number: {response.data.page_number}')
print(f'Page Size: {response.data.page_size}')
print(f'Total Pages: {response.data.total_pages}')
print(f'Total Records: {response.data.total_records}')
print('Reports:')

for report in response.data.reports:
    print(f' Id: {report.id}')
    print(f' Name: {report.name}')
    print(f' Description: {report.description}')
```
