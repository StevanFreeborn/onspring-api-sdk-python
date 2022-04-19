from OnspringClient import OnspringClient
from configparser import ConfigParser
from Models import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

def GetRecordsByAppIdTest():

    request = GetRecordsByAppRequest(240, dataFormat=DataFormat.Raw.name)

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
            print(f'  Type: {field.type}, FieldId: {field.fieldId}, Value: {field.getValue()}')

def SaveFileTest():

    filePath = 'C:\\Users\\sfree\\OneDrive\\Desktop\\Test Attachment.txt'

    request = SaveFileRequest(
        60, 
        6989, 
        'Test Attachment.text', 
        filePath, 'text/plain', 
        'Updating record with attachment')

    response = onspringClient.SaveFile(request)

    print(response.statusCode)
    print(response.data.id)