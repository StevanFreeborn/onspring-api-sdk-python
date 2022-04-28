from audioop import mul
import datetime
import uuid

from requests import Response

from Enums import *
from decimal import Decimal
from datetime import datetime
from Helpers import parseDate

# generic

class ApiResponse:
    """
    An object to represent a response to a request made by an `OnspringClient`.

    Attributes:
        statusCode (`int`): The http status code of the response.
        data: If the success was successful will contain the response data deserialized to custom python objects.
        message (`str`): A message that may provide more detail about the requests success or failure.
        raw (`requests.Response`): Exposes the raw response object of the request if you'd like to handle it directly.
    """

    def __init__(self, statusCode=None, data=None, message=None, raw=None):
        self.statusCode = statusCode
        self.isSuccessful = int(statusCode) < 400
        self.data = data
        self.message = message
        self.raw = raw

class PagingRequest:
    """
    An object to represent the page number and page size of a paginated request made by an `OnspringClient`.

    Attributes:
        pageNumber (`int`): The page number that will be requested.
        pageSize (`int`): The size of the page that will be requested.
    """

    def __init__(self, pageNumber: int, pageSize: int):
        self.pageNumber = pageNumber
        self.pageSize = pageSize

#app specific

class App:
    """
    An object to represent an Onspring app.

    Attributes:
        href (`str`): The href for the Onspring app.
        id (`int`): The id of the Onspring app.
        name (`str`): The name of the Onspring app.
    """

    def __init__(self, href: str, id: int, name: str):
        self.href = href
        self.id = id
        self.name = name

class GetAppsResponse:
    """
    An object to represent a paginated response to a request made by an `OnspringClient` to request a collection of `Models.App`s.

    Attributes:
        pageNumber (`int`): The page number returned.
        pageSize (`int`): The size of the page returned.
        totalPages (`int`): The total number of pages for the request.
        totalRecords (`int`): The total records for the request.
        apps (`list[Models.App]`): The apps requested.
    """

    def __init__(self, pageNumber: int, pageSize: int, totalPages:int , totalRecords: int, apps: list[App]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.apps = apps

class GetAppByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a `Models.App`.

    Attributes:
        app (`Models.App`): The requested app.
    """

    def __init__(self, app: App):
        self.app = app

class GetAppsByIdsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a collection of `Models.App`s.

    Attributes:
        count (`int`): The number of apps requested.
        apps (`list[Models.App]`): The apps requested.
    """

    def __init__(self, count: int, apps: list[App]):
        self.count = count
        self.apps = apps

# field specific

class ListValue:
    def __init__(self, id: int, name: str, sortOrder: int, numericValue: Decimal, color: str):
        self.id = id
        self.name = name
        self.sortOrder = sortOrder

        if numericValue != None:
            self.numericValue = Decimal(numericValue)
        else:
            self.numericValue = numericValue
        
        self.color = color

    def AsString(self):
        return f'Id: {self.id}, Name: {self.name}, Value: {self.numericValue}, Sort Order: {self.sortOrder}, Color: {self.color}'

class Field:
    def __init__(
        self, id: int, 
        appId: int, 
        name: str, 
        type: str, 
        status: str, 
        isRequired: bool, 
        isUnique: bool, 
        listId: int=None, 
        values: list[ListValue]=None, 
        multiplicity: str=None,
        outputType: str=None
        ):

        self.id = id
        self.appId = appId
        self.name = name
        self.type = type
        self.status = status
        self.isRequired = isRequired
        self.isUnique = isUnique
        self.listId = listId
        self.values = values
        self.outputType = outputType
        self.multiplicity = multiplicity

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
    """
    An object to represent all the necessary information needed to make a successful 'OnspringClient.SaveFile' request.

    Attributes:
        recordId (`int`): The unique id of the record where you want to save the file.
        fieldId (`int`): The unique id of the field where you want to save the file.
        fileName (`str`): The name of the file you want to save.
        filePath (`str`): The path to the file you want to save.
        contentType (`str`): The content type of the file you want to save.
        notes (`str`): An option note about the file.
        notes (`datetime`): An optional date noting when the file was modified.
    """
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

# record specific

class RecordFieldValue:
    def __init__(self, fieldId: int, value: str, type: str=None):
        self.type = type
        self.fieldId = fieldId
        self.value = value

    def AsString(self):
        
        if self.type != ResultValueType.String.name:
            return None

        return StringFieldValue(self.fieldId, self.value).value

    def AsInteger(self):
        
        if self.type != ResultValueType.Integer.name:
            return None
        
        return IntegerFieldValue(self.fieldId, int(self.value)).value

    def AsDecimal(self):
        
        if self.type != ResultValueType.Decimal.name:
            return None
        
        return DecimalFieldValue(self.fieldId, Decimal(self.value)).value

    def AsDate(self):
        
        if self.type != ResultValueType.Date.name:
            return None

        date = parseDate(self.value)

        return DateFieldValue(self.fieldId, date).value

    def AsGuid(self):

        if self.type != ResultValueType.Guid.name:
            return None
        
        return GuidFieldValue(self.fieldId, uuid.UUID(self.value)).value
        
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

        return TimeSpanValue(self.fieldId, data).value

    def AsStringList(self):

        if self.type != ResultValueType.StringList.name:
            return None
        
        strings = [str(string) for string in self.value]

        return StringListValue(self.fieldId, strings).value

    def AsIntegerList(self):
        
        if self.type != ResultValueType.IntegerList.name:
            return None

        integers = [int(integer) for integer in self.value]
            
        return IntegerListValue(self.fieldId, integers).value

    def AsGuidList(self):

        if self.type != ResultValueType.GuidList.name:
            return None

        guids = []

        for guid in self.value:
            guids.append(uuid.UUID(guid))
            
        return GuidListValue(self.fieldId, guids).value

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

        return AttachmentListValue(self.fieldId, attachments).value

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
        
        return ScoringGroupListValue(self.fieldId, scoringGroups).value

    def AsFileList(self):
        
        if self.type != ResultValueType.FileList.name:
            return None

        files = [int(file) for file in self.value]
            
        return FileListValue(self.fieldId, files).value

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

    def GetResultValueString(self):
        match self.type:
            case ResultValueType.String.name:
                return self.AsString()

            case ResultValueType.Integer.name:
                return self.AsInteger()

            case ResultValueType.Decimal.name:
                return self.AsDecimal()

            case ResultValueType.Date.name:
                return self.AsDate()

            case ResultValueType.TimeSpan.name:
                data = self.AsTimeSpan()
                return f'Quantity: {data.quantity}, Increment: {data.increment}, Recurrence: {data.recurrence}, EndByDate: {data.endByDate}, EndAfterOccurrences: {data.endAfterOccurrences}'
            
            case ResultValueType.Guid.name:
                return self.AsGuid()
            
            case ResultValueType.StringList.name:
                data = self.AsStringList()
                return f'{",".join(data)}'
            
            case ResultValueType.IntegerList.name:
                data = self.AsIntegerList()
                return f'{",".join([str(i) for i in data])}'
            
            case ResultValueType.GuidList.name:
                data = self.AsGuidList()
                return f'{",".join([str(guid) for guid in data])}'
            
            case ResultValueType.AttachmentList.name:
                data = self.AsAttachmentList()

                strings = []

                for attachment in data:
                    string = f'FileId: {attachment.fileId}, FileName: {attachment.fileName}, Notes: {attachment.notes}, StorageLocation: {attachment.storageLocation}'
                    strings.append(string)
                
                return f'{"; ".join(strings)}'
            
            case ResultValueType.ScoringGroupList.name:
                data = self.AsScoringGroupList()

                strings = []

                for scoringGroup in data:
                    string = f'ListValueId: {scoringGroup.listValueId}, Name: {scoringGroup.name}, Score: {scoringGroup.score}, Max Score: {scoringGroup.maximumScore}'
                    strings.append(string)

                return f'{"; ".join(strings)}'
            
            case ResultValueType.FileList.name:
                data = self.AsFileList()
                return f'{",".join([str(i) for i in data])}'

class Record:
    def __init__(self, appId: int, fields: list[RecordFieldValue], recordId: int=None):
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

class QueryRecordsRequest:
    def __init__(self, appId: int, filter: str, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name, pagingRequest: PagingRequest=PagingRequest(1,50)):
        self.appId = appId
        self.filter = filter
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat
        self.pagingRequest = pagingRequest

class GetRecordsResponse:
    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, records: list[Record]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.records = records

class GetRecordByIdRequest:
    def __init__(self, appId: int, recordId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):
        self.appId = appId
        self.recordId = recordId
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat

class GetBatchRecordsRequest:
    def __init__(self, appId: int, recordIds: list[int], fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):
        self.appId = appId
        self.recordIds = recordIds
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat

class GetBatchRecordsResponse:
    def __init__(self, count: int, records: list[Record]):
        self.count = count
        self.records = records

class AddOrUpdateRecordResponse:
    def __init__(self, id: int, warnings: list[str]=[]):
        self.id = id
        self.warnings = warnings

class DeleteBatchRecordsRequest:
    def __init__(self, appId: int, recordIds: list[int]):
        self.appId = appId
        self.recordIds = recordIds

# field types

class StringFieldValue(RecordFieldValue):
    def __init__(self, fieldId: int, value):
        self.type = ResultValueType.String.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class IntegerFieldValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: int):
        self.type = ResultValueType.Integer.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class DecimalFieldValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: Decimal):
        self.type = ResultValueType.Decimal.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class DateFieldValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: datetime):
        self.type = ResultValueType.Date.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class GuidFieldValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: uuid.UUID):
        self.type = ResultValueType.Guid.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class TimeSpanData:
    def __init__(self, quantity: Decimal, increment: Increment, recurrence: Recurrence=None, endByDate: datetime=None, endAfterOccurrences: int=None):
        self.quantity = quantity
        self.increment = increment
        self.recurrence = recurrence
        self.endByDate = endByDate
        self.endAfterOccurrences = endAfterOccurrences

    def AsString(self):
        if self.endByDate != None:
            formattedDate = self.endByDate.strftime("%m/%d/%Y %I:%M %p")
            return f'Every {self.quantity} {self.increment} End By {formattedDate}'
        elif self.endAfterOccurrences != None:
            return f'Every {self.quantity} {self.increment} End After {self.endAfterOccurrences}'
        else:
            return f'{self.quantity} {self.increment}'

class TimeSpanValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: TimeSpanData):
        self.type = ResultValueType.TimeSpan.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class StringListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[str]):
        self.type = ResultValueType.StringList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class IntegerListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[int]):
        self.type = ResultValueType.IntegerList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class GuidListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[uuid.UUID]):
        self.type = ResultValueType.GuidList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class Attachment:
    def __init__(self, fileId: int, fileName: str, notes: str, storageLocation: str):
        self.fileId = fileId
        self.fileName = fileName
        self.notes = notes
        self.storageLocation = storageLocation

class AttachmentListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[Attachment]):
        self.type = ResultValueType.AttachmentList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class FileListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[int]):
        self.type = ResultValueType.FileList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class ScoringGroup:
    def __init__(self, listValueId: uuid.UUID, name: str, score: Decimal, maximumScore: Decimal):
        self.listValueId = listValueId
        self.name = name
        self.score = score
        self.maximumScore = maximumScore

class ScoringGroupListValue(RecordFieldValue):
    def __init__(self, fieldId: int, value: list[ScoringGroup]):
        self.type = ResultValueType.ScoringGroupList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

# report specific

class GetReportByIdRequest:
    def __init__(self, reportId: int, apiDataFormat: str=DataFormat.Raw.name, dataType: str=ReportDataType.ReportData.name):
        self.reportId = reportId
        self.apiDataFormat = apiDataFormat
        self.dataType = dataType

class Row:
    def __init__(self, recordId: int, cells: list[str]):
        self.recordId = recordId
        self.cells = cells

class GetReportByIdResponse:
    def __init__(self, columns: list[str], rows: list[Row]):
        self.columns = columns
        self.rows = rows

class Report:
    def __init__(self, appId: int, id: int, name: str, description: str):
        self.appId = appId
        self.id = id
        self.name = name
        self.description = description

class GetReportsByAppIdResponse:
    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, reports: list[Report]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.reports = reports