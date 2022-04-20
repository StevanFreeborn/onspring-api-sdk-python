import mimetypes
import os
import sys

from OnspringClient import OnspringClient
from configparser import ConfigParser
from Helpers import GetResultValueString

from Models import *
from Enums import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspring = OnspringClient(url, key)

def main():

    if not len(sys.argv) > 1:
        print('No valid command given')
        return

    command = sys.argv[1].lower()

    if command =='connect':
        PrintCanConnect(onspring)
        
    if command == 'getapps':
        PrintGetApps(onspring)
    
    if command == 'getappbyid':
        PrintGetAppById(onspring, 195)
        
    if command == 'getappsbyids':
        PrintGetAppsByIds(onspring, [195, 240])
    
    if command == 'savefile':
        PrintSaveFile(
            onspring,
            'C:\\Users\\sfree\\OneDrive\\Desktop\\Test Attachment.txt',
            60,
            6989
        )
    
    if command == 'getrecordsbyappid':
        PrintGetRecordsByAppId(onspring, 195)
        return
    
    if command == 'getrecordbyid':
        PrintGetRecordById(onspring, 195, 3,dataFormat=DataFormat.Raw.name)
        return
    
    if command == 'deleterecord':
        PrintDeleteRecord(onspring, 195, sys.argv[2])
        return
    
    if command == 'getrecordsbyids':
        PrintGetRecordsByIds(onspring, 195, [1, 2], [6983, 6984])
        return

    if command == 'queryrecords':
        fieldId = 6983
        operator = 'eq'
        value = '\'Test Task 5\''
        PrintQueryRecords(onspring, 195, f'{fieldId} {operator} {value}')
        return

    if command == 'addrecord':

        fields = [
            StringFieldValue(6983, 'A New Test Task'),
            StringFieldValue(6984, 'This is a test task.')
        ]

        PrintAddOrUpdateRecord(onspring, 195, fields)
        return

    if command == 'updaterecord':

        fields = [
            StringFieldValue(6983, 'Updated'),
            StringFieldValue(6984, 'Updated')
        ]

        PrintAddOrUpdateRecord(onspring, 195, fields, 60)
        return

    print('No valid command given')
    return

#connectivity

def PrintCanConnect(client: OnspringClient):
    
    print(client.CanConnect())

# apps

def PrintGetApps(client: OnspringClient):
    
    response = client.GetApps()
    
    print(f'Status Code: {response.statusCode}')
    print(f'Page Size: {response.data.pageSize}')
    print(f'Page Number: {response.data.pageNumber}')
    print(f'Total Pages: {response.data.totalPages}')
    print(f'Total Records: {response.data.totalRecords}')
    print('----')

    for app in response.data.apps:
        print(f'Id: {app.id}')
        print(f'Name: {app.name}')
        print(f'href: {app.href}')
        print('--')

    print('----')

def PrintGetAppById(client: OnspringClient, appId: int):
    
    response = client.GetAppById(appId)

    print(f'Status Code: {response.statusCode}')
    print(f'id: {response.data.app.id}')
    print(f'Name: {response.data.app.name}')
    print(f'href: {response.data.app.href}')

def PrintGetAppsByIds(client: OnspringClient, appIds: list[int]):

    response = client.GetAppsByIds(appIds)

    print(f'Status Code: {response.statusCode}')
    print(f'Count: {response.data.count}')
    print('----')

    for app in response.data.apps:
        print(f'Id: {app.id}')
        print(f'Name: {app.name}')
        print(f'href: {app.href}')
        print('--')

    print('----')

# records

def PrintGetRecordsByAppId(client: OnspringClient, appId: int):

    request = GetRecordsByAppRequest(appId, dataFormat=DataFormat.Raw.name)

    response = client.GetRecordsByAppId(request)

    print(f'Status Code: {response.statusCode}')
    print(f'Page Size: {response.data.pageSize}')
    print(f'Page Number: {response.data.pageNumber}')
    print(f'Total Pages: {response.data.totalPages}')
    print(f'Total Records: {response.data.totalRecords}')
    print('----')

    for record in response.data.records:
        print(f'AppId: {record.appId}')
        print(f'RecordId: {record.recordId}')
        print('--')

        for field in record.fields:
            print(f'Type: {field.type}')
            print(f'FieldId: {field.fieldId}')
            print(f'Value: {GetResultValueString(field)}')
            print('--')
        
        print('----')

def PrintGetRecordById(client: OnspringClient, appId: int, recordId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):

    request = GetRecordByIdRequest(
        appId,
        recordId,
        fieldIds,
        dataFormat)

    response = client.GetRecordById(request)

    print(f'Status Code: {response.statusCode}')
    print('----')
    print(f'AppId: {response.data.appId}')
    print(f'RecordId: {response.data.recordId}')
    print('--')

    for field in response.data.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {GetResultValueString(field)}')
        print('--')
    
    print('----')

def PrintDeleteRecord(client: OnspringClient, appId: int, recordId: int):

    response = client.DeleteRecordById(appId, recordId)

    print(f'Status Code: {response.statusCode}')
    print(f'Message: {response.message}')

def PrintGetRecordsByIds(client: OnspringClient, appId: int, recordIds: list[int], fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):

    request = GetBatchRecordsRequest(
        appId,
        recordIds,
        fieldIds,
        dataFormat)

    response = client.GetRecordsByIds(request)

    print(f'Status Code: {response.statusCode}')
    print(f'Count: {response.data.count}')
    print('----')

    for record in response.data.records:
        print(f'AppId: {record.appId}')
        print(f'RecordId: {record.recordId}')
        print('--')

        for field in record.fields:
            print(f'Type: {field.type}')
            print(f'FieldId: {field.fieldId}')
            print(f'Value: {GetResultValueString(field)}')
            print('--')
        
        print('----')


def PrintQueryRecords(client: OnspringClient, appId: int, filter: str, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name, pagingRequest: PagingRequest=PagingRequest(1,50)):

    request = QueryRecordsRequest(
        appId,
        filter,
        fieldIds,
        dataFormat,
        pagingRequest)

    response = client.QueryRecords(request)

    print(f'Status Code: {response.statusCode}')
    print(f'Page Size: {response.data.pageSize}')
    print(f'Page Number: {response.data.pageNumber}')
    print(f'Total Pages: {response.data.totalPages}')
    print(f'Total Records: {response.data.totalRecords}')
    print('----')

    for record in response.data.records:
        print(f'AppId: {record.appId}')
        print(f'RecordId: {record.recordId}')
        print('--')

        for field in record.fields:
            print(f'Type: {field.type}')
            print(f'FieldId: {field.fieldId}')
            print(f'Value: {GetResultValueString(field)}')
            print('--')
        
        print('----')

def PrintAddOrUpdateRecord(client: OnspringClient, appId: int, fields: list[RecordFieldValue], recordId: int=None):

    record = Record(
        appId,
        fields,
        recordId)

    response = client.AddOrUpdateRecord(record)

    print(response.status_code)
    print(response.text)
    print(response.request.body)
    

# files

def PrintSaveFile(client: OnspringClient, filePath: str, recordId: int, fieldId: int, notes: str=None, modifiedDate: datetime=None):

    filePath = filePath
    fileName = os.path.basename(filePath)
    contentType = mimetypes.guess_type(filePath)

    request = SaveFileRequest(
        recordId, 
        fieldId, 
        fileName, 
        filePath, 
        contentType, 
        notes,
        modifiedDate)

    response = client.SaveFile(request)

    print(f'Status Code: {response.statusCode}')
    print(f'File Id: {response.data.id}')

if __name__ == "__main__":
    main()