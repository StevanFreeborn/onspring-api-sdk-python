from OnspringClient import OnspringClient
from configparser import ConfigParser
from Models import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

request = GetRecordsByAppRequest(195, dataFormat=DataFormat.Raw.name)

response = onspringClient.GetRecordsByAppId(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f' AppId: {record.appId}')
    print(f' RecordId: {record.recordId}')

    for field in record.fields:
        if field.type == ResultValueType.Decimal.name:
            print(f'  Type: {field.type}, FieldId: {field.fieldId}, Value: {field.AsDecimal()}')
            print(field.AsDecimal())