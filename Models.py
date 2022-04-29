import datetime
import uuid

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
    An object to represent a paginated response to a request made by an `OnspringClient` to request a collection of Onspring apps.

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
    An object to represent a response to a request made by an `OnspringClient` to request an Onspring app.

    Attributes:
        app (`Models.App`): The requested app.
    """

    def __init__(self, app: App):
        self.app = app

class GetAppsByIdsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring apps.

    Attributes:
        count (`int`): The number of apps requested.
        apps (`list[Models.App]`): The apps requested.
    """

    def __init__(self, count: int, apps: list[App]):
        self.count = count
        self.apps = apps

# field specific

class ListValue:
    """
    An object to represent an Onspring list value.

    Attributes:
        id (`int`): The id of the Onspring list value.
        name (`str`): The list value's name.
        sortOrder (`int`): The list value's sort order in respect to other values in the same list.
        numericalValue (`Decimal`): The numeric value assigned to the list value.
        color (`str`): The color assigned to the list value.
    """

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
        """
        Gets the list value as a comma separated string of it's properties and their values.

        Args:
            None

        Returns:
            A `str` representation of the list value object.
        """

        return f'Id: {self.id}, Name: {self.name}, Value: {self.numericValue}, Sort Order: {self.sortOrder}, Color: {self.color}'

class Field:
    """
    An object to represent an Onspring field.

    Attributes:
        id (`int`): The id of the Onspring field.
        appId ('int'): The id of the Onspring app where the field resides.
        name (`str`): The name of the field.
        type (`str`): The type of the field.
        status (`str`): The stuat of the field.
        isRequired (`bool`): Indicates whether the field is required in Onspring or not.
        isUnique (`bool`): Indicates whether the field requires unique values in Onspring or not.
        listId (`int`): The id of the fields list if applicable. Used for list fields and formula fields with list output type.
        values (`list[Models.ListValue]`): The values of the fields list if applicable. Used for list fields and formula fields with list output type.
        multiplicity (`str`): The multiplicity of the field if applicable. Used for list fields, reference fields, and formula fields with a list output type.
        outputType (`str`): The output type of the field if applicable. Used for formula fields.
    """

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
    """
    An object to represent a response to a request made by an `OnspringClient` to request an Onspring field.

    Attributes:
        field (`Models.Field`): The requested field.
    """

    def __init__(self, field: Field):
        self.field = field

class GetFieldsByIdsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring fields.

    Attributes:
        count (`int`): The number of fields requested.
        fields (`list[Models.Field]`): The fields requested.
    """

    def __init__(self, count: int, fields: list[Field]):
        self.count = count
        self.fields = fields

class GetFieldsByAppIdResponse:
    """
    An object to represent a paginated response to a request made by an `OnspringClient` to request a collection of Onspring fields.

    Attributes:
        pageNumber (`int`): The page number returned.
        pageSize (`int`): The size of the page returned.
        totalPages (`int`): The total number of pages for the request.
        totalRecords (`int`): The total records for the request.
        fields (`list[Models.Field]`): The fields requested.
    """

    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, fields: list[Field]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.fields = fields

# file specific

class File:
    """
    An object to represent a file stored in Onsprng.

    Attributes:
        name (`str`): The name of the file.
        contentType (`str`): The content type of the file.
        contentLength (`int`): The length of the file's content.
        content (`bytes`): The content of the file.
    """

    def __init__(self, name: str, contentType: str, contentLength: int, content: bytes):
        self.name = name
        self.contentType = contentType
        self.contentLength = contentLength
        self.content = content

class FileInfo:
    """
    An object to represent the metadata for a file stored in Onspring.

    Attributes:
        type (`str`): The type of file as stored in Onspring Attachment or Image.
        contentType (`str`): The content type of the file itself.
        name (`str`): The name of the file
        createdDate (`datetime`): The created date of the file.
        modifiedDate (`datetime`): The modified date of the file.
        owner (`str`): The owner of the file.
        fileHref (`str`): The href for the file.
    """

    def __init__(self, type: str, contentType: str, name: str, createdDate: datetime, modifiedDate: datetime, owner: str, fileHref: str):
        self.type = type
        self.contentType = contentType
        self.name = name
        self.createdDate = createdDate
        self.modifiedDate = modifiedDate
        self.owner = owner
        self.fileHref = fileHref

class GetFileInfoByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a info for a file in Onspring.

    Attributes:
        fileInfo (`Models.FileInfo`): The file info requested.
    """

    def __init__(self, fileInfo: FileInfo):
        self.fileInfo = fileInfo

class GetFileByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a file in Onspring.

    Attributes:
        file (`Models.File`): The file requested.
    """

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
    """
    An object to represent a response to a request made by an `OnspringClient` to save a file in Onspring.

    Attributes:
        id (`int`): The id of the file saved in Onspring.
    """

    def __init__(self, id: int):
        self.id = id

# list specific

class ListItemRequest:
    """
    An object to represent the necessary information for adding or updating a list value. If no id is provided the list value will be added. If an id is provided then an attempt will be made to find that list value and update it.

    Attributes:
        listId (`int`): The id of the parent list that the list value belongs to.
        name (`str`): The name of the list value.
        id (`uuid`): The id of the list value.
        numericValue (`int`): The numeric value assigned to the list value.
        color (`str`): The color value assigned to the list value.
    """

    def __init__(self, listId: int, name: str, id: uuid=None, numericValue: int=None, color: str=None):
        self.listId = listId
        self.name = name
        self.id = id
        self.numericValue = numericValue
        self.color = color

class AddOrUpdateListItemResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to add or update a list value in Onspring.

    Attributes:
        id (`int`): The id of the list value updated or added in Onspring.
    """

    def __init__(self, id: uuid):
        self.id = id

# record specific

class RecordFieldValue:
    """
    An object to represent the value in a field in an Onspring record.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`str`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: str, type: str=None):
        self.fieldId = fieldId
        self.value = value
        self.type = type

    def AsString(self):
        """
        If the `Models.RecordFieldValue` type is String will return the value property as a `str` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `str`.
        """
        
        if self.type != ResultValueType.String.name:
            return None

        return StringFieldValue(self.fieldId, self.value).value

    def AsInteger(self):
        """
        If the `Models.RecordFieldValue` type is Integer will return the value property as an `int` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as an `int`.
        """
        
        if self.type != ResultValueType.Integer.name:
            return None
        
        return IntegerFieldValue(self.fieldId, int(self.value)).value

    def AsDecimal(self):
        """
        If the `Models.RecordFieldValue` type is Decimal will return the value property as a `Decimal` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `Decimal`.
        """
        
        if self.type != ResultValueType.Decimal.name:
            return None
        
        return DecimalFieldValue(self.fieldId, Decimal(self.value)).value

    def AsDate(self):
        """
        If the `Models.RecordFieldValue` type is Date will return the value property as a `datetime` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `datetime`.
        """
        
        if self.type != ResultValueType.Date.name:
            return None

        date = parseDate(self.value)

        return DateFieldValue(self.fieldId, date).value

    def AsGuid(self):
        """
        If the `Models.RecordFieldValue` type is Guid will return the value property as an `UUID` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as an `UUID`.
        """

        if self.type != ResultValueType.Guid.name:
            return None
        
        return GuidFieldValue(self.fieldId, uuid.UUID(self.value)).value
        
    def AsTimeSpan(self):
        """
        If the `Models.RecordFieldValue` type is TimeSpan will return the value property as a `Model.TimeSpanData` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `Model.TimeSpanData`.
        """

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
        """
        If the `Models.RecordFieldValue` type is StringList will return the value property as a `list[str]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[str]`.
        """

        if self.type != ResultValueType.StringList.name:
            return None
        
        strings = [str(string) for string in self.value]

        return StringListValue(self.fieldId, strings).value

    def AsIntegerList(self):
        """
        If the `Models.RecordFieldValue` type is IntegerList will return the value property as a `list[int]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[int]`.
        """
        
        if self.type != ResultValueType.IntegerList.name:
            return None

        integers = [int(integer) for integer in self.value]
            
        return IntegerListValue(self.fieldId, integers).value

    def AsGuidList(self):
        """
        If the `Models.RecordFieldValue` type is GuidList will return the value property as a `list[UUID]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[UUID]`.
        """

        if self.type != ResultValueType.GuidList.name:
            return None

        guids = []

        for guid in self.value:
            guids.append(uuid.UUID(guid))
            
        return GuidListValue(self.fieldId, guids).value

    def AsAttachmentList(self):
        """
        If the `Models.RecordFieldValue` type is AttachmentList will return the value property as a `list[Models.Attachment]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[Models.Attachment]`.
        """

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
        """
        If the `Models.RecordFieldValue` type is ScoringGroupList will return the value property as a `list[Models.ScoringGroup]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[Models.ScoringGroup]`.
        """

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
        """
        If the `Models.RecordFieldValue` type is FileList will return the value property as a `list[int]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[int]`.
        """
        
        if self.type != ResultValueType.FileList.name:
            return None

        files = [int(file) for file in self.value]
            
        return FileListValue(self.fieldId, files).value

    def getValue(self):
        """
        Will determine the appropriate way to return the fields value based on it's type.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as the appropriate object.
        """

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
        """
        Will return the value property regardless of the field value's type as a string.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a string.
        """
        if self.type == ResultValueType.String.name:
            return self.AsString()

        elif self.type == ResultValueType.Integer.name:
            return self.AsInteger()

        elif self.type == ResultValueType.Decimal.name:
            return self.AsDecimal()

        elif self.type == ResultValueType.Date.name:
            return self.AsDate()

        elif self.type ==  ResultValueType.TimeSpan.name:
            data = self.AsTimeSpan()
            return f'Quantity: {data.quantity}, Increment: {data.increment}, Recurrence: {data.recurrence}, EndByDate: {data.endByDate}, EndAfterOccurrences: {data.endAfterOccurrences}'
            
        elif self.type == ResultValueType.Guid.name:
            return self.AsGuid()
            
        elif self.type ==  ResultValueType.StringList.name:
            data = self.AsStringList()
            return f'{",".join(data)}'
            
        elif self.type == ResultValueType.IntegerList.name:
            data = self.AsIntegerList()
            return f'{",".join([str(i) for i in data])}'
            
        elif self.type == ResultValueType.GuidList.name:
            data = self.AsGuidList()
            return f'{",".join([str(guid) for guid in data])}'
            
        elif self.type == ResultValueType.AttachmentList.name:
            data = self.AsAttachmentList()

            strings = []

            for attachment in data:
                string = f'FileId: {attachment.fileId}, FileName: {attachment.fileName}, Notes: {attachment.notes}, StorageLocation: {attachment.storageLocation}'
                strings.append(string)
            
            return f'{"; ".join(strings)}'
            
        elif self.type == ResultValueType.ScoringGroupList.name:
            data = self.AsScoringGroupList()

            strings = []

            for scoringGroup in data:
                string = f'ListValueId: {scoringGroup.listValueId}, Name: {scoringGroup.name}, Score: {scoringGroup.score}, Max Score: {scoringGroup.maximumScore}'
                strings.append(string)

            return f'{"; ".join(strings)}'

        elif self.type == ResultValueType.FileList.name:
            data = self.AsFileList()
            return f'{",".join([str(i) for i in data])}'

        else:
            return None

class Record:
    """
    An object to represent an Onspring record.

    Attributes:
        appId ('int'): The id of the Onspring app where the record resides.
        recordId (`int`): The id of the Onspring record.
        fields (`list[Models.RecordFieldValue]`): The record's field values.
    """
    
    def __init__(self, appId: int, fields: list[RecordFieldValue], recordId: int=None):
        self.appId = appId
        self.recordId = recordId
        self.fields = fields

class GetRecordsByAppRequest:
    """
    An object to represent all the necessary information for making a succcessful request to get a collection of Onspring records.

    Attributes:
        appId (`int`): The id for the Onspring app where the records reside.
        fieldIds (`list[int]`): The ids for the fields in the Onspring app that should be included for each record in the response.
        dataFormat (`str`): The format of the response data.
        pagingRequest (`Models.PagingRequest`): Used to set the page number and page size of the request. By default the these will be 1 and 50 respectively.
    """

    def __init__(self, appId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name, pagingRequest: PagingRequest=PagingRequest(1,50)):
        self.appId = appId
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat
        self.pageSize = pagingRequest.pageSize
        self.pageNumber = pagingRequest.pageNumber

class QueryRecordsRequest:
    """
    An object to represent all the necessary information for making a succcessful request to get a collection of Onspring records based on a specific criteria. For more information on constructing a proper filter please refer to the official Onspring API guide: https://shorturl.at/cnsFK.

    Attributes:
        appId (`int`): The id for the Onspring app where the records reside.
        filter (`str`): The criteria used to determine what records should be included in the response.
        fieldIds (`list[int]`): The ids for the fields in the Onspring app that should be included for each record in the response.
        dataFormat (`str`): The format of the response data.
        pagingRequest (`Models.PagingRequest`): Used to set the page number and page size of the request. By default the these will be 1 and 50 respectively.
    """

    def __init__(self, appId: int, filter: str, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name, pagingRequest: PagingRequest=PagingRequest(1,50)):
        self.appId = appId
        self.filter = filter
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat
        self.pagingRequest = pagingRequest

class GetRecordsResponse:
    """
    An object to represent a paginated response to a request made by an `OnspringClient` to request a collection of Onspring records.

    Attributes:
        pageNumber (`int`): The page number returned.
        pageSize (`int`): The size of the page returned.
        totalPages (`int`): The total number of pages for the request.
        totalRecords (`int`): The total records for the request.
        records (`list[Models.Record]`): The records requested.
    """

    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, records: list[Record]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.records = records

class GetRecordByIdRequest:
    """
    An object to represent all the necessary information for making a succcessful request to get an Onspring record by its id.

    Attributes:
        appId (`int`): The id for the Onspring app where the record resides.
        recordId (`int`): The id for the record being requested.
        fieldIds (`list[int]`): The ids for the fields in the Onspring app that should be included for each record in the response.
        dataFormat (`str`): The format of the response data.
    """
    def __init__(self, appId: int, recordId: int, fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):
        self.appId = appId
        self.recordId = recordId
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat

class GetBatchRecordsRequest:
    """
    An object to represent all the necessary information for making a succcessful request to get a batch of Onspring records by their ids.

    Attributes:
        appId (`int`): The id for the Onspring app where the records reside.
        recordId (`list[int]`): The ids for the records being requested.
        fieldIds (`list[int]`): The ids for the fields in the Onspring app that should be included for each record in the response.
        dataFormat (`str`): The format of the response data.
    """

    def __init__(self, appId: int, recordIds: list[int], fieldIds: list[int]=[], dataFormat: str=DataFormat.Raw.name):
        self.appId = appId
        self.recordIds = recordIds
        self.fieldIds = fieldIds
        self.dataFormat = dataFormat

class GetBatchRecordsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring records.

    Attributes:
        count (`int`): The number of records requested.
        records (`list[Models.Record]`): The records requested.
    """

    def __init__(self, count: int, records: list[Record]):
        self.count = count
        self.records = records

class AddOrUpdateRecordResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to add or update an Onspring record.
    
    Attributes:
        id (`int`): The id of the Onspring record that was added or updated.
        warnings ('list[str]'): A list of warnings.
    """

    def __init__(self, id: int, warnings: list[str]=[]):
        self.id = id
        self.warnings = warnings

class DeleteBatchRecordsRequest:
    """
    An object to represent all the necessary information for making a succcessful request to delete a batch of Onspring records by their ids.

    Attributes:
        appId (`int`): The id for the Onspring app where the records reside.
        recordId (`list[int]`): The ids for the records being deleted.
    """

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