# Onspring API Python SDK

The python SDK for **version 2** of the Onspring API is meant to simplify development in Python for Onspring customers who want to build integrations with their Onspring instance.

**Note:**
This is an unofficial SDK for the Onspring API. It was not built in consultation with Onspring Technologies LLC or a member of their development team.

This SDK was developed independently using their existing C# SDK, their swagger page, and api documentation with the intention of making development of integrations done in Python with an Onspring instance quicker and more convenient.

## Dependencies

### Python

Requires use of Python 3.6.0 or later.

### Requests

All methods for the `OnspringClient` make use of the [Requests](https://docs.python-requests.org/en/latest/) library to interact with the endpoints of version 2 of the Onspring API.

## Installation

Install the SDK using pip:

`pip install onspring-api-sdk-python`

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
from OnspringClient import OnspringClient
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

### Verify connectivity

```python
canConnect = client.CanConnect()

if canConnect:
    print('Connected successfully')
else:
    print('Attempt to connect failed')
```

### Get Apps

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

### Get App By Id

Returns an Onspring app or survey according to provided id.

```python
response = client.GetAppById(appId)

print(f'Status Code: {response.statusCode}')
print(f'id: {response.data.app.id}')
print(f'Name: {response.data.app.name}')
print(f'href: {response.data.app.href}')
```

### Get Apps By Ids

Returns a collection of Onspring apps and/or surveys according to provided ids.

```python
response = client.GetAppsByIds([195, 240])

print(f'Status Code: {response.statusCode}')
print(f'Count: {response.data.count}')

for app in response.data.apps:
    print(f'Id: {app.id}')
    print(f'Name: {app.name}')
    print(f'href: {app.href}')
```

### Get Field By Id

```python
```

### Get Fields By Ids

```python
```

### Get Fields By App Id

Returns a paged collection of apps and/or surveys that can be paged through. By default the page size is 50 and page number is 1.

```python
response = client.GetFieldById(9686)

print(f'Status Code: {response.statusCode}')

if response.isSuccessful:
    PrintField(response.data.field)
else:
    print(f'Message: {response.message}')
```

You can set your own page size and page number (max is 1,000) as well.

```python
pagingRequest = PagingRequest(1, 100)
response = client.GetFieldById(9686, pagingRequest)

print(f'Status Code: {response.statusCode}')

if response.isSuccessful:
    PrintField(response.data.field)
else:
    print(f'Message: {response.message}')
```

Example `PrintField` method:

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

### Get File Info By Id

```python
```

### Delete File By Id

```python
```

### Get File By Id

```python
```

### Save File

```python
```

### Add Or Update List Value

```python
```

### Delete List Value

### Get Records By App Id

```python
```

### Get Record By Id

```python
```

### Delete Record By Id

```python
```

### Get Records By Ids

```python
```

### Query Records

```python
```

### Add or Update A Record

```python
```

### Delete Records By Ids

```python
```

### Get Report By Id

```python
```

### Get Reports By App Id

```python
```
