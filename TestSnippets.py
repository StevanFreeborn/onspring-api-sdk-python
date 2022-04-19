from OnspringClient import OnspringClient
from configparser import ConfigParser
from Helpers import GetResultValueString

from Models import *
from Enums import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

def main():
    GetRecordsByAppIdTest()



# apps

def GetRecordsByAppIdTest():

    request = GetRecordsByAppRequest(240, dataFormat=DataFormat.Raw.name)

    response = onspringClient.GetRecordsByAppId(request)

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
            print(f'Value: {GetResultValueString(field)}')

# files

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

if __name__ == "__main__":
    main()