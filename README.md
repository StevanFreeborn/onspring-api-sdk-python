# Onspring API Python SDK

The python SDK for **version 2** of the Onspring API is meant to simplify development in Python for Onspring customers who want to build integrations with their Onspring instance.

**Note:**
This is an unofficial SDK for the Onspring API. It was not built in consultation with Onspring Technologies LLC or a member of their development team.

This SDK was developed independently using their existing C# SDK, their swagger page, and api documentation as the starting point with the intention of making development of integrations done in Python with an Onspring instance quicker and more convenient.

## Dependencies

### Python

Requires use of Python 3.10.0 or later.

### Requests

All methods for the `OnspringClient` make use of the [Requests](https://docs.python-requests.org/en/latest/) library to interact with the endpoints of version 2 of the Onspring API.

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

- `baseUrl` - currently this should always be: `https://api.onspring.com`
- `apiKey` - the value obtained by following the steps in the **API Key** section

It is best practice to read these values in from a configuration file for both flexibility and security purposes.

Example `config.ini` file:

```ini
[prod]
key = 000000ffffff000000ffffff/00000000-ffff-0000-ffff-000000000000
url = https://api.onspring.com
```

Example constructing `OnspringClient`:

```python
from OnspringApiSdk.OnspringClient import OnspringClient
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

client = OnspringClient(url, key)
```

### `ApiResponse`

Each `OnspringClient` method - aside from `CanConnect` - returns an `ApiResponse` object which will have the following properties:

- `statusCode` - The http status code of the response.
- `data` - If the request was successful will contain the response data deserialized to custom python objects.
- `message` - A message that may provide more detail about the requests success or failure.
- `raw` - Exposes the raw response object of the request if you'd like to handle it directly.

The goal with this `ApiResponse` object is to provide the flexibility to do with the response what you'd like as well as already having the raw JSON response deserialized to python objects.

If you do want to handle and/or manipulate the response object yourself you will want to use the value of the `ApiResponse`'s `raw` property which will be a [`Response`](https://docs.python-requests.org/en/latest/user/advanced/#request-and-response-objects) object from the [Requests](https://docs.python-requests.org/en/latest/) library.

## Full API Documentation

You may wish to refer to the full [Onspring API documentation](https://software.onspring.com/hubfs/Training/Admin%20Guide%20-%20v2%20API.pdf) when determining which values to pass as parameters to some of the `OnspringClient` methods. There is also a [swagger page](https://api.onspring.com/swagger/index.html) that you can use for making exploratory requests.

## Example Code

The examples that follow assume you have created an `OnspringClient` as described in the **Start Coding** section.

### Connectivity

#### Verify connectivity

```python
canConnect = client.CanConnect()

if canConnect:
    print('Connected successfully')
else:
    print('Attempt to connect failed')
```

### Apps

#### Get Apps

Returns a paged collection of apps and/or surveys that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.GetApps()
  
print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

You can set your own page size and page number (max is 1,000) as well.

```python
from OnspringApiSdk.Models import PagingRequest

pagingRequest = PagingRequest(1, 100)
response = client.GetApps(pagingRequest)
  
print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

#### Get App By Id

Returns an Onspring app or survey according to provided id.

```python
response = client.GetAppById(appId=195)

print(f'Status Code: {response.statusCode}')
print(f'id: {response.data.app.id}')
print(f'Name: {response.data.app.name}')
print(f'href: {response.data.app.href}')
```

#### Get Apps By Ids

Returns a collection of Onspring apps and/or surveys according to provided ids.

```python
response = client.GetAppsByIds(appIds=[195, 240])

print(f'Status Code: {response.statusCode}')
print(f'Count: {response.data.count}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

### Fields

#### Helpers

Example `PrintField` method referenced in following examples.

```python
def PrintField(field: Field):
    
    print('Field:')
    print(f' Id: {field.id}')
    print(f' App Id: {field.appId}')
    print(f' Name: {field.name}')
    print(f' Type: {field.type}')
    print(f' Status: {field.status}')
    print(f' IsRequired: {field.isRequired}')
    print(f' IsUnique: {field.isUnique}')

    if field.type == 'Formula':

        print(f' Output Type: {field.outputType}')

        if field.outputType == 'ListValue':

            print(f' Multiplicity: {field.multiplicity}')
            print(' Values:')

            for value in field.values:

                print(f'  {value.AsString()}')

    if field.type == 'List':

        print(f' Multiplicity: {field.multiplicity}')
        print(' Values:')

        for value in field.values:

            print(f'  {value.AsString()}')
```

#### Get Field By Id

Returns an Onspring field according to provided id.

```python
response = client.GetFieldById(fieldId=9686)

print(f'Status Code: {response.statusCode}')
PrintField(response.data.field)
```

#### Get Fields By Ids

Returns a collection of Onspring fields according to provided ids.

```python
response = client.GetFieldsByIds(fieldIds=[9686, 9687])

print(f'Status Code: {response.statusCode}')
print(f'Count: {response.data.count}')

for field in response.data.fields:
    PrintField(field)
```

#### Get Fields By App Id

Returns a paged collection of fields that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.GetFieldsByAppId(appId=195)
    
    print(f'Status Code: {response.statusCode}')
    print(f'Page Size: {response.data.pageSize}')
    print(f'Page Number: {response.data.pageNumber}')
    print(f'Total Pages: {response.data.totalPages}')
    print(f'Total Records: {response.data.totalRecords}')

    for field in response.data.fields:
        PrintField(field)
```

You can set your own page size and page number (max is 1,000) as well.

```python
from OnspringApiSdk.Models import PagingRequest

pagingRequest = PagingRequest(1, 100)

response = client.GetFieldsByAppId(appId=195, pagingRequest)
    
    print(f'Status Code: {response.statusCode}')
    print(f'Page Size: {response.data.pageSize}')
    print(f'Page Number: {response.data.pageNumber}')
    print(f'Total Pages: {response.data.totalPages}')
    print(f'Total Records: {response.data.totalRecords}')

    for field in response.data.fields:
        PrintField(field)
```

### Files

#### Get File Info By Id

Returns the Onspring file's metadata.

```python
response = client.GetFileInfoById(recordId=1, fieldId=6990, fileId=274)

print(f'Status Code: {response.statusCode}')
print(f'Name: {response.data.fileInfo.name}')
print(f'Type: {response.data.fileInfo.type}')
print(f'Owner: {response.data.fileInfo.owner}')
print(f'Content Type: {response.data.fileInfo.contentType}')
print(f'Created Date: {response.data.fileInfo.createdDate}')
print(f'Modified Date: {response.data.fileInfo.modifiedDate}')
print(f'File Href: {response.data.fileInfo.fileHref}')
```

#### Get File By Id

Returns the file itself.

```python
response = client.GetFileById(recordId=1, fieldId=6990, fileId=274)

print(f'Status Code: {response.statusCode}')
print(f'Name: {response.data.file.name}')
print(f'Content Type: {response.data.file.contentType}')
print(f'Content Length: {response.data.file.contentLength}')

filePath = f'C:\\Users\\sfree\\Documents\\Temp\\{response.data.file.name}'

with open(filePath, "wb") as file:
    
    file.write(response.data.file.content)

print(f'File Location: {filePath}')
```

#### Save File

```python
from OnspringApiSdk.Models import SaveFileRequest
import os
import mimetypes

filePath = 'C:\\Users\\sfree\\Documents\\Temp\\Test Attachment.txt'
fileName = os.path.basename(filePath)
contentType = mimetypes.guess_type(filePath)[0]

request = SaveFileRequest(
    recordId=60, 
    fieldId=6989, 
    fileName,
    filePath, 
    contentType, 
    notes='Initial revision',
    modifiedDate=datetime.now())

response = client.SaveFile(request)

print(f'Status Code: {response.statusCode}')
print(f'File Id: {response.data.id}')
```

#### Delete File By Id

```python
response = client.DeleteFileById(recordId=60, fieldId=6989, fileId=231)

print(f'Status Code: {response.statusCode}')
print(f'Message: {response.message}')
```

### Lists

#### Add Or Update List Value

To add a list value don't provide an id value.

```python
from OnspringApiSdk.Models import ListItemRequest

request = ListItemRequest(
        listId=906, 
        name='Not Started', 
        id='', 
        numericValue=0, 
        color='#ffffff')

response = client.AddOrUpdateListItem(request)

print(f'Status Code: {response.statusCode}')
print(f'Id: {response.data.id}')
```

To update a list value provide an id value.

```python
from OnspringApiSdk.Models import ListItemRequest

request = ListItemRequest(
        listId=906, 
        name='Pending', 
        id='4118d53a-9121-4345-8682-07f23d606daa', 
        numericValue=0, 
        color='#ffffff')

response = client.AddOrUpdateListItem(request)

print(f'Status Code: {response.statusCode}')
print(f'Id: {response.data.id}')
```

#### Delete List Value

```python
response = client.DeleteListItem(listId=906, itemId='36f94d8c-2b9d-465e-9ad1-ede04109efc9')

print(f'Status Code: {response.statusCode}')
print(f'Message: {response.message}')
```

### Records

#### Get Records By App Id

Returns a paged colletion of records that can be paged through. By default the page size is 50 and page number is 1.

```python
request = GetRecordsByAppRequest(appId=195)

response = client.GetRecordsByAppId(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

You can set your own page size and page number (max is 1,000) as well. In addition to specifying what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from OnspringApiSdk.Models import PagingRequest, GetRecordsByAppRequest
from OnspringApiSdk.Enums import DataFormat 

pagingRequest = PagingRequest(1,10)

request = GetRecordsByAppRequest(
    appId=195,
    fieldIds=[9686],
    dataFormat=DataFormat.Formatted.name,
    pagingRequest)

response = client.GetRecordsByAppId(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

#### Get Record By Id

Returns an onspring record based on the provided app and record ids.

```python
from OnspringApiSdk.Models import GetRecordByIdRequest

request = GetRecordByIdRequest(appId=195, recordId=60)

response = client.GetRecordById(request)

print(f'Status Code: {response.statusCode}')
print(f'AppId: {response.data.appId}')
print(f'RecordId: {response.data.recordId}')

for field in response.data.fields:
    print(f'Type: {field.type}')
    print(f'FieldId: {field.fieldId}')
    print(f'Value: {field.GetResultValueString()}')
```

You can also specify what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from OnspringApiSdk.Models import GetRecordByIdRequest
from OnspringApiSdk.Enums import DataFormat

request = GetRecordByIdRequest(
    appId=195, 
    recordId=60,
    fieldIds=[9686],
    dataFormat=DataFormat.Formatted.name)

response = client.GetRecordById(request)

print(f'Status Code: {response.statusCode}')
print(f'AppId: {response.data.appId}')
print(f'RecordId: {response.data.recordId}')

for field in response.data.fields:
    print(f'Type: {field.type}')
    print(f'FieldId: {field.fieldId}')
    print(f'Value: {field.GetResultValueString()}')
```

#### Delete Record By Id

```python
response = client.DeleteRecordById(appId=195, recordId=60)

print(f'Status Code: {response.statusCode}')
print(f'Message: {response.message}')
```

#### Get Records By Ids

Returns a collection of Onspring records based on the provided appId and recordIds.

```python
from OnspringApiSdk.Models import GetBatchRecordsRequest

request = GetBatchRecordsRequest(appId=195, recordIds=[1, 2, 3])

response = client.GetRecordsByIds(request)

print(f'Status Code: {response.statusCode}')
print(f'Count: {response.data.count}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

You can also specify what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from OnspringApiSdk.Models import GetBatchRecordsRequest
from OnspringApiSdk.Enums import DataFormat

request = GetBatchRecordsRequest(
    appId=195, 
    recordIds=[1, 2, 3],
    fieldIds=[9686],
    dataFormat=DataFormat.Formatted.name)

response = client.GetRecordsByIds(request)

print(f'Status Code: {response.statusCode}')
print(f'Count: {response.data.count}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

#### Query Records

Returns a paged colletion of records based on a criteria that can be paged through. By default the page size is 50 and page number is 1.

```python
from OnspringApiSdk.Models import QueryRecordsRequest

fieldId = 6983
operator = 'eq'
value = '\'Test Task 5\''

request = QueryRecordsRequest(appId=195, filter=f'{fieldId} {operator} {value}')

response = client.QueryRecords(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

You can set your own page size and page number (max is 1,000) as well. In addition to specifying what field values to return and in what format (Raw vs. Formatted) to return them.

```python
from OnspringApiSdk.Models import PagingRequest, QueryRecordsRequest
from OnspringApiSdk.Enums import DataFormat

pagingRequest = PagingRequest(1, 10)
fieldId = 6983
operator = 'eq'
value = '\'Test Task 5\''

request = QueryRecordsRequest(
    appId=195, 
    filter=f'{fieldId} {operator} {value}',
    fieldIds=[9686],
    dataFormat=DataFormat.Formatted.name,
    pagingRequest)

response = client.QueryRecords(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f'AppId: {record.appId}')
    print(f'RecordId: {record.recordId}')

    for field in record.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')
```

For further details on constructing the `filter` parameter please refer to the [documentation](https://software.onspring.com/hubfs/Training/Admin%20Guide%20-%20v2%20API.pdf) for v2 of the Onspring API.

#### Add or Update A Record

You can add a record by not providing a record id value. If successful will return the id of the added record.

```python
from OnspringApiSdk.Models import StringFieldValue, GuidFieldValue, DateFieldValue, IntegerListValue, Record

fields = []

status = uuid.UUID('4118d53a-9121-4345-8682-07f23d606daa')
dueDate = datetime.utcnow()

fields.append(StringFieldValue(6983, 'Test Task via API'))
fields.append(StringFieldValue(6984, 'This is a task.'))
fields.append(GuidFieldValue(6986, status))
fields.append(DateFieldValue(6985, dueDate))
fields.append(IntegerListValue(6987, [4]))

record = Record(
    appId=195, 
    fields)

response = client.AddOrUpdateRecord(record)

print(f'Status Code: {response.statusCode}')
print(f'Id: {response.data.id}')
for warning in response.data.warnings:
    print(f'Warning: {warning}')
```

You can update a record by providing its id. If successful will return the id of record updated.

```python
from OnspringApiSdk.Models import StringFieldValue, GuidFieldValue, DateFieldValue, IntegerListValue, Record

fields = []

status = uuid.UUID('1c1c5f7e-cd03-4b70-9790-0f83b24b5863')
dueDate = datetime.utcnow()

fields.append(StringFieldValue(6983, 'Test Task via API'))
fields.append(StringFieldValue(6984, 'This is a task.'))
fields.append(GuidFieldValue(6986, status))
fields.append(DateFieldValue(6985, dueDate))
fields.append(IntegerListValue(6987, [4]))

record = Record(
    appId=195, 
    fields, 
    recordId=103)

response = client.AddOrUpdateRecord(record)

print(f'Status Code: {response.statusCode}')
print(f'Id: {response.data.id}')
for warning in response.data.warnings:
    print(f'Warning: {warning}')
```

#### Delete Records By Ids

```python
from OnspringApiSdk.Models import DeleteBatchRecordsRequest

request = DeleteBatchRecordsRequest(appId=195, recordIds=[1, 2, 3])

response = client.DeleteRecordsByIds(request)

print(f'Status Code: {response.statusCode}')
print(f'Message: {response.message}')
```

### Reports

#### Get Report By Id

Returns the report for the provided id.

```python
from OnspringApiSdk.Models import GetReportByIdRequest

request = GetReportByIdRequest(reportId=53)

response = client.GetReportById(request)

print(f'Status Code: {response.statusCode}')
print('Columns:')
print(f'{", ".join(response.data.columns)}')
print('Rows:')
for row in response.data.rows:
    print(f'Record Id {row.recordId}: {", ".join([str(cell) for cell in row.cells])}')
```

You can also specify the format of the data in the report as well as whether you are requesting the report's data or its chart data.

```python
from OnspringApiSdk.Models import GetReportByIdRequest
from OnspringApiSdk.Enums import DataFormat, ReportDataType

request = GetReportByIdRequest(
    reportId=53,
    apiDataFormat=DataFormat.Formatted.name,
    dataFormat=ReportDataType.ChartData.name)

response = client.GetReportById(request)

print(f'Status Code: {response.statusCode}')
print('Columns:')
print(f'{", ".join(response.data.columns)}')
print('Rows:')
for row in response.data.rows:
    print(f'Record Id {row.recordId}: {", ".join([str(cell) for cell in row.cells])}')
```

#### Get Reports By App Id

Returns a paged collection of reports that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.GetReportsByAppId(appId=195)

print(f'Status Code: {response.statusCode}')
print(f'App Id: {appId}')
print('Reports:')

for report in response.data.reports:
    print(f' Id: {report.id}')
    print(f' Name: {report.name}')
    print(f' Description: {report.description}')
```

You can set your own page size and page number (max is 1,000) as well.

```python
from OnspringApiSdk.Models import PagingRequest

pagingRequest = PagingRequest(1,10)

response = client.GetReportsByAppId(appId=195, pagingRequest)

print(f'Status Code: {response.statusCode}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Page Number: {response.data.pageSize}')
print(f'Page Number: {response.data.totalPages}')
print(f'Page Number: {response.data.totalRecords}')
print(f'App Id: {appId}')
print('Reports:')

for report in response.data.reports:
    print(f' Id: {report.id}')
    print(f' Name: {report.name}')
    print(f' Description: {report.description}')
```
