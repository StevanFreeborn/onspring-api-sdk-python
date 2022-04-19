from http import client
import mimetypes
import os

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

    # PrintGetApps(onspring)

    PrintGetAppById(onspring, 195)
    
    # PrintSaveFile(
    #     onspring,
    #     'C:\\Users\\sfree\\OneDrive\\Desktop\\Test Attachment.txt',
    #     60,
    #     6989
    # )

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