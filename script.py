from OnspringClient import OnspringClient
from configparser import ConfigParser
from Models import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

request = GetRecordsByAppRequest(195)

response = onspringClient.GetRecordsByAppId(request)

print(f'Status Code: {response.statusCode}')
print(f'Page Size: {response.data.pageSize}')
print(f'Page Number: {response.data.pageNumber}')
print(f'Total Pages: {response.data.totalPages}')
print(f'Total Records: {response.data.totalRecords}')

for record in response.data.records:
    print(f' AppId: {record.appId}')
    print(f' RecordId: {record.recordId}')

    for value in record.fieldData:
        print(f'  Type: {value.type}, FieldId: {value.fieldId}, Value: {value.value}')

