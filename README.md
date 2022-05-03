# Onspring API Python SDK

The python SDK for **version 2** of the Onspring API is meant to simplify development in Python for Onspring customers who want to build integrations with their Onspring instance.

**Note:**
This is an unofficial SDK for the Onspring API. It was not built in consultation with Onspring Technologies LLC or a member of their development team.

This SDK was developed independently using their existing C# SDK as a guide and with the intention of making development of integrations done in Python with an Onspring instance quicker and more convenient.

## Dependencies

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

The most common way to use the SDK is to create an OnspringClient instance and call its methods. Its constructor requires two parameters:

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

### Get App By Id

```python
```

### Get Apps By Ids

```python
```

### Get Field By Id

```python
```

### Get Fields By Ids

```python
```

### Get Fields By App Id

```python
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
