import json
import mimetypes
import os

from requests import request

from OnspringClient import OnspringClient

from Models import *
from Enums import *

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

    for app in response.data.apps:
        print(f'Id: {app.id}')
        print(f'Name: {app.name}')
        print(f'href: {app.href}')

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

    for app in response.data.apps:
        print(f'Id: {app.id}')
        print(f'Name: {app.name}')
        print(f'href: {app.href}')

# fields

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

def PrintGetFieldById(client: OnspringClient, fieldId: int):

    response = client.GetFieldById(fieldId)

    print(f'Status Code: {response.statusCode}')


    if response.isSuccessful:
        PrintField(response.data.field)
    else:
        print(f'Message: {response.message}')

# files

def PrintGetFileById(client: OnspringClient, recordId: int, fieldId: int, fileId: int):

    response = client.GetFileById(recordId, fieldId, fileId)

    print(f'Status Code: {response.statusCode}')
    print(f'Name: {response.data.file.name}')
    print(f'Content Type: {response.data.file.contentType}')
    print(f'Content Length: {response.data.file.contentLength}')

def PrintGetFileInfoById(client: OnspringClient, recordId: int, fieldId: int, fileId: int):

    response = client.GetFileInfoById(recordId, fieldId, fileId)

    print(f'Status Code: {response.statusCode}')
    print(f'Name: {response.data.fileInfo.name}')
    print(f'Type: {response.data.fileInfo.type}')
    print(f'Owner: {response.data.fileInfo.owner}')
    print(f'Content Type: {response.data.fileInfo.contentType}')
    print(f'Created Date: {response.data.fileInfo.createdDate}')
    print(f'Modified Date: {response.data.fileInfo.modifiedDate}')
    print(f'File Href: {response.data.fileInfo.fileHref}')

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

# records

def PrintGetRecordsByAppId(client: OnspringClient, appId: int):

    request = GetRecordsByAppRequest(appId, dataFormat=DataFormat.Raw.name)

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

def PrintGetRecordById(client: OnspringClient, appId: int, recordId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):

    request = GetRecordByIdRequest(
        appId,
        recordId,
        fieldIds,
        dataFormat)

    response = client.GetRecordById(request)

    print(f'Status Code: {response.statusCode}')
    print(f'AppId: {response.data.appId}')
    print(f'RecordId: {response.data.recordId}')

    for field in response.data.fields:
        print(f'Type: {field.type}')
        print(f'FieldId: {field.fieldId}')
        print(f'Value: {field.GetResultValueString()}')

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

    for record in response.data.records:
        print(f'AppId: {record.appId}')
        print(f'RecordId: {record.recordId}')

        for field in record.fields:
            print(f'Type: {field.type}')
            print(f'FieldId: {field.fieldId}')
            print(f'Value: {field.GetResultValueString()}')

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

    for record in response.data.records:
        print(f'AppId: {record.appId}')
        print(f'RecordId: {record.recordId}')

        for field in record.fields:
            print(f'Type: {field.type}')
            print(f'FieldId: {field.fieldId}')
            print(f'Value: {field.GetResultValueString()}')

def PrintAddOrUpdateRecord(client: OnspringClient, appId: int, fields: list[RecordFieldValue], recordId: int=None):

    record = Record(
        appId,
        fields,
        recordId)

    response = client.AddOrUpdateRecord(record)

    print(f'Status Code: {response.statusCode}')
    print(f'Id: {response.data.id}')
    for warning in response.data.warnings:
        print(f'Warning: {warning}')

def PrintDeleteRecordsByIds(client: OnspringClient, appId: int, recordIds: list[int]):

    request = DeleteBatchRecordsRequest(appId, recordIds)

    response = client.DeleteRecordsByIds(request)

    print(f'Status Code: {response.statusCode}')
    print(f'Message: {response.message}')
    
# reports

def PrintGetReportById(client: OnspringClient, reportId: int, apiDataFormat: str=DataFormat.Raw.name, dataFormat: str=ReportDataType.ReportData.name):

    request = GetReportByIdRequest(reportId, apiDataFormat, dataFormat)

    response = client.GetReportById(request)

    print(f'Status Code: {response.statusCode}')
    print('Columns:')
    print(f'{", ".join(response.data.columns)}')
    print('Rows:')
    for row in response.data.rows:
        print(f'Record Id {row.recordId}: {", ".join([str(cell) for cell in row.cells])}')

def PrintGetReportsByAppId(client: OnspringClient, appId: int, pagingRequest: PagingRequest=PagingRequest(1,50)):

    response = client.GetReportsByAppId(appId, pagingRequest)

    print(f'Status Code: {response.statusCode}')
    print(f'App Id: {appId}')
    print('Reports:')

    for report in response.data.reports:
        print(f' Id: {report.id}')
        print(f' Name: {report.name}')
        print(f' Description: {report.description}')