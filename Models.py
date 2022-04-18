import datetime
from decimal import Decimal
import uuid

from Enums import DataFormat, ResultValueType

# generic

class ApiResponse:
    def __init__(self, statusCode=None, data=None, message=None, headers=None, responseText=None):
        self.statusCode = statusCode
        self.isSuccessful = int(statusCode) < 400
        self.data = data
        self.message = message
        self.headers=None
        self.responseText = responseText

class PagingRequest:
    def __init__(self, pageNumber: int, pageSize: int):
        self.pageNumber = pageNumber
        self.pageSize = pageSize

#app specific

class App:
    def __init__(self, href: str, id: int, name: str):
        self.href = href
        self.id = id
        self.name = name

class GetAppsResponse:
    def __init__(self, pageNumber: int, pageSize: int, totalPages:int , totalRecords: int, apps: list[App]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.apps = apps

class GetAppByIdResponse:
    def __init__(self, app: App):
        self.app = app

class GetAppsByIdsResponse:
    def __init__(self, count: int, apps: list[App]):
        self.count = count
        self.apps = apps

# field specific

class Field:
    def __init__(self, id: int, appId: int, name: str, type: str, status: str, isRequired: bool, isUnique: bool):
        self.id = id
        self.appId = appId
        self.name = name
        self.type = type
        self.status = status
        self.isRequired = isRequired
        self.isUnique = isUnique

class GetFieldByIdResponse:
    def __init__(self, field: Field):
        self.field = field

class GetFieldsByIdsResponse:
    def __init__(self, count: int, fields: list[Field]):
        self.count = count
        self.fields = fields

class GetFieldsByAppIdResponse:
    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, fields: list[Field]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.fields = fields

# file specific

class File:
    def __init__(self, name: str, contentType: str, contentLength: int, content: bytes):
        self.name = name
        self.contentType = contentType
        self.contentLength = contentLength
        self.content = content

class FileInfo:
    def __init__(self, type: str, contentType: str, name: str, createdDate: str, modifiedDate: str, owner: str, fileHref: str):
        self.type = type
        self.contentType = contentType
        self.name = name
        self.createdDate = createdDate
        self.modifiedDate = modifiedDate
        self.owner = owner
        self.fileHref = fileHref

class GetFileInfoByIdResponse:
    def __init__(self, fileInfo: FileInfo):
        self.fileInfo = fileInfo

class GetFileByIdResponse:
    def __init__(self, file: File):
        self.file = file

class SaveFileRequest:
    def __init__(self, recordId: int, fieldId: int, fileName: str, filePath: str, contentType: str, notes: str=None, modifiedDate: datetime=None):
        self.recordId = recordId
        self.fieldId = fieldId
        self.notes = notes
        self.modifiedDate = modifiedDate
        self.fileName = fileName
        self.filePath = filePath
        self.contentType = contentType

class SaveFileResponse:
    def __init__(self, id: int):
        self.id = id

# list specific

class ListItemRequest:
    def __init__(self, listId: int, name: str, id: uuid=None, numericValue: int=None, color: str=None):
        self.listId = listId
        self.name = name
        self.id = id
        self.numericValue = numericValue
        self.color = color

class AddOrUpdateListItemResponse:
    def __init__(self, id: uuid):
        self.id = id

# field types

class StringFieldValue:
    def __init__(self, value: str, fieldId: int):
        self.type = ResultValueType.String.name
        self.fieldId = fieldId
        self.value = value

class IntegerFieldValue:
    def __init__(self, value: int, fieldId: int):
        self.type = ResultValueType.Integer.name
        self.value = value
        self.fieldId = fieldId

class DecimalFieldValue:
    def __init__(self, value: Decimal, fieldId: int):
        self.type = ResultValueType.Decimal.name
        self.value = value
        self.fieldId = fieldId

class DateFieldValue:
    def __init__(self, value: datetime, fieldId: int):
        self.type = ResultValueType.Date.name
        self.value = value
        self.fieldId = fieldId

class GuidFieldValue:
    def __init__(self, value: uuid, fieldId: int):
        self.type = ResultValueType.Guid.name
        self.value = value
        self.fieldId = fieldId

class TimeSpanData:
    def __init__(self, quantity: Decimal, ):
        pass

class TimeSpanValue:
    def __init__(self, value: uuid, fieldId: int):
        self.type = ResultValueType.Guid.name
        self.value = value
        self.fieldId = fieldId

# record specific

class RecordFieldValue:
    def __init__(self, type: str, fieldId: int, value: str):
        self.type = type
        self.fieldId = fieldId
        self.value = value

    def AsString(self):
        
        if self.type != ResultValueType.String.name:
            return None

        return StringFieldValue(str(self.value), self.fieldId).value

    def AsInt(self):
        
        if self.type != ResultValueType.Integer.name:
            return None
        
        return IntegerFieldValue(int(self.value), self.fieldId).value

    def AsDecimal(self):
        
        if self.type != ResultValueType.Decimal.name:
            return None
        
        return DecimalFieldValue(Decimal(self.value), self.fieldId).value

    def AsDate(self):
        
        if self.type != ResultValueType.Date.name:
            return None

        for format in ["%Y-%m-%dT%H:%M:%S.%fZ","%Y-%m-%dT%H:%M:%SZ"]:
            try:
                date = datetime.datetime.strptime(self.value, format)
            except ValueError:
                pass

        return DateFieldValue(date, self.fieldId).value

    def AsGuid(self):

        if self.type != ResultValueType.Guid.name:
            return None
        
        return GuidFieldValue(uuid.UUID(self.value), self.fieldId).value
        
    def AsTimeSpan():
        return

class Record:
    def __init__(self, appId: int, recordId: int, fieldData: list[RecordFieldValue]):
        self.appId = appId
        self.recordId = recordId
        self.fieldData = fieldData

class GetRecordsByAppRequest:
    def __init__(self, appId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name, pagingRequest: PagingRequest=PagingRequest(1,50)):
        self.appId = appId
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat
        self.pageSize = pagingRequest.pageSize
        self.pageNumber = pagingRequest.pageNumber

class GetRecordsByAppResponse:
    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, records: list[Record]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.records = records