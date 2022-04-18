import datetime
import uuid

from Enums import *
from decimal import Decimal
from datetime import datetime
from Helpers import parseDate

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
    def __init__(self, type: str, contentType: str, name: str, createdDate: datetime, modifiedDate: datetime, owner: str, fileHref: str):
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
        self.fieldId = fieldId
        self.value = value

class IntegerFieldValue:
    def __init__(self, value: int, fieldId: int):
        self.value = value
        self.fieldId = fieldId

class DecimalFieldValue:
    def __init__(self, value: Decimal, fieldId: int):
        self.value = value
        self.fieldId = fieldId

class DateFieldValue:
    def __init__(self, value: datetime, fieldId: int):
        self.value = value
        self.fieldId = fieldId

class GuidFieldValue:
    def __init__(self, value: uuid.UUID, fieldId: int):
        self.value = value
        self.fieldId = fieldId

class TimeSpanData:
    def __init__(self, quantity: Decimal, increment: str, recurrence: str=None, endByDate: datetime=None, endAfterOccurrences: int=None):
        self.quantity = quantity
        self.increment = increment
        self.recurrence = recurrence
        self.endByDate = endByDate
        self.endAfterOccurrences = endAfterOccurrences

class TimeSpanValue:
    def __init__(self, value: TimeSpanData, fieldId: int):
        self.value = value
        self.fieldId = fieldId

class StringListValue:
    def __init__(self, value: list[str], fieldId: int):
        self.value = value
        self.fieldId = fieldId

class IntegerListValue:
    def __init__(self, value: list[int], fieldId: int):
        self.value = value
        self.fieldId = fieldId

class GuidListValue:
    def __init__(self, value: list[uuid.UUID], fieldId: int):
        self.value = value
        self.fieldId = fieldId

class Attachment:
    def __init__(self, fileId: int, fileName: str, notes: str, storageLocation: str):
        self.fileId = fileId
        self.fileName = fileName
        self.notes = notes
        self.storageLocation = storageLocation

class AttachmentListValue:
    def __init__(self, value: list[Attachment], fieldId: int):
        self.value = value
        self.fieldId = fieldId

class FileListValue:
    def __init__(self, value: list[int], fieldId: int):
        self.value = value
        self.fieldId = fieldId

class ScoringGroup:
    def __init__(self, listValueId: uuid.UUID, name: str, score: Decimal, maximumScore: Decimal):
        self.listValueId = listValueId
        self.name = name
        self.score = score
        self.maximumScore = maximumScore

class ScoringGroupListValue:
    def __init__(self, value: list[ScoringGroup], fieldId: int):
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

        return StringFieldValue(self.value, self.fieldId).value

    def AsInteger(self):
        
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

        date = parseDate(self.value)

        return DateFieldValue(date, self.fieldId).value

    def AsGuid(self):

        if self.type != ResultValueType.Guid.name:
            return None
        
        return GuidFieldValue(uuid.UUID(self.value), self.fieldId).value
        
    def AsTimeSpan(self):

        if self.type != ResultValueType.TimeSpan.name:
            return None
        
        value = dict(self.value)

        quantity = value.get('quantity')
        increment = value.get('increment')
        recurrence = value.get('recurrence')
        endByDate = value.get('endByDate')
        endAfterOccurrences = value.get('endAfterOccurrences')

        endByDate = parseDate(endByDate)

        data = TimeSpanData(
            quantity,
            increment,
            recurrence,
            endByDate,
            endAfterOccurrences)

        return TimeSpanValue(data, self.fieldId).value

    def AsStringList(self):

        if self.type != ResultValueType.StringList.name:
            return None
            
        return StringListValue(self.value, self.fieldId).value

    def AsIntegerList(self):
        
        if self.type != ResultValueType.IntegerList.name:
            return None
            
        return IntegerListValue(self.value, self.fieldId).value

    def AsGuidList(self):

        if self.type != ResultValueType.GuidList.name:
            return None

        guids = []

        for guid in self.value:
            guids.append(uuid.UUID(guid))
            
        return GuidListValue(guids, self.fieldId).value

    def AsAttachmentList(self):

        if self.type != ResultValueType.AttachmentList.name:
            return None

        attachments = []

        for attachment in self.value:

            attachment = dict(attachment)

            attachment = Attachment(
                attachment.get('fileId'),
                attachment.get('fileName'),
                attachment.get('notes'),
                attachment.get('storageLocation'))

            attachments.append(attachment)

        return AttachmentListValue(attachments, self.fieldId).value

    def AsScoringGroupList(self):

        if self.type != ResultValueType.ScoringGroupList.name:
            return

        scoringGroups = []

        for scoringGroup in self.value:

            scoringGroup = dict(scoringGroup)

            scoringGroup = ScoringGroup(
                uuid.UUID(scoringGroup.get('listValueId')),
                scoringGroup.get('name'),
                Decimal(scoringGroup.get('score')),
                Decimal(scoringGroup.get('maximumScore')))

            scoringGroups.append(scoringGroup)
        
        return ScoringGroupListValue(scoringGroups, self.fieldId).value

    def AsFileList(self):
        
        if self.type != ResultValueType.FileList.name:
            return None
            
        return FileListValue(self.value, self.fieldId).value

    def getValue(self):

        if self.type == ResultValueType.String.name:
            return self.AsString()
        elif self.type == ResultValueType.Integer.name:
            return self.AsInteger()
        elif self.type == ResultValueType.Decimal.name:
            return self.AsDecimal()
        elif self.type == ResultValueType.Date.name:
            return self.AsDate()
        elif self.type == ResultValueType.TimeSpan.name:
            return self.AsTimeSpan()
        elif self.type == ResultValueType.Guid.name:
            return self.AsGuid()
        elif self.type == ResultValueType.StringList.name:
            return self.AsStringList()
        elif self.type == ResultValueType.IntegerList.name:
            return self.AsIntegerList()
        elif self.type == ResultValueType.GuidList.name:
            return self.AsGuidList()
        elif self.type == ResultValueType.AttachmentList.name:
            return self.AsAttachmentList()
        elif self.type == ResultValueType.ScoringGroupList.name:
            return self.AsScoringGroupList()
        elif self.type == ResultValueType.FileList.name:
            return self.AsFileList()
        else:
            return None

class Record:
    def __init__(self, appId: int, recordId: int, fields: list[RecordFieldValue]):
        self.appId = appId
        self.recordId = recordId
        self.fields = fields

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