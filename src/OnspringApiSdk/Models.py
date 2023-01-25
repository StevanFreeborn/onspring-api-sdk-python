import datetime
import uuid

from OnspringApiSdk.Enums import *
from decimal import Decimal
from datetime import datetime
from OnspringApiSdk.Helpers import parseDate
from requests import Response

# paging

class PagingRequest:
    """
    An object to represent the page number and page size of a paginated request made by an `OnspringClient`.

    Attributes:
        pageNumber (`int`): The page number that will be requested.
        pageSize (`int`): The size of the page that will be requested.
    """

    def __init__(self, pageNumber: int, pageSize: int):
        self.pageNumber:int = pageNumber
        self.pageSize:int = pageSize

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
        self.href:str = href
        self.id:int = id
        self.name:str = name

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
        self.pageNumber:int = pageNumber
        self.pageSize:int = pageSize
        self.totalPages:int = totalPages
        self.totalRecords:int = totalRecords
        self.apps:list[App] = apps

class GetAppByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request an Onspring app.

    Attributes:
        app (`Models.App`): The requested app.
    """

    def __init__(self, app: App):
        self.app:App = app

class GetAppsByIdsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring apps.

    Attributes:
        count (`int`): The number of apps requested.
        apps (`list[Models.App]`): The apps requested.
    """

    def __init__(self, count: int, apps: list[App]):
        self.count:int = count
        self.apps:list[App] = apps

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
        self.id:int = id
        self.name:str = name
        self.sortOrder:int = sortOrder

        if numericValue != None:
            self.numericValue:Decimal = Decimal(numericValue)
        else:
            self.numericValue:Decimal = numericValue
        
        self.color:str = color

    def AsString(self) -> str:
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

        self.id:int = id
        self.appId:int = appId
        self.name:str = name
        self.type:str = type
        self.status:str = status
        self.isRequired:bool = isRequired
        self.isUnique:bool = isUnique
        self.listId:int = listId
        self.values:list[ListValue] = values
        self.outputType:str = outputType
        self.multiplicity:str = multiplicity

class GetFieldByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request an Onspring field.

    Attributes:
        field (`Models.Field`): The requested field.
    """

    def __init__(self, field: Field):
        self.field:Field = field

class GetFieldsByIdsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring fields.

    Attributes:
        count (`int`): The number of fields requested.
        fields (`list[Models.Field]`): The fields requested.
    """

    def __init__(self, count: int, fields: list[Field]):
        self.count:int = count
        self.fields:list[Field] = fields

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
        self.pageNumber:int = pageNumber
        self.pageSize:int = pageSize
        self.totalPages:int = totalPages
        self.totalRecords:int = totalRecords
        self.fields:list[Field] = fields

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
        self.name:str = name
        self.contentType:str = contentType
        self.contentLength:int = contentLength
        self.content:bytes = content

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
        self.type:str = type
        self.contentType:str = contentType
        self.name:str = name
        self.createdDate:datetime = createdDate
        self.modifiedDate:datetime = modifiedDate
        self.owner:str = owner
        self.fileHref:str = fileHref

class GetFileInfoByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a info for a file in Onspring.

    Attributes:
        fileInfo (`Models.FileInfo`): The file info requested.
    """

    def __init__(self, fileInfo: FileInfo):
        self.fileInfo:FileInfo = fileInfo

class GetFileByIdResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a file in Onspring.

    Attributes:
        file (`Models.File`): The file requested.
    """

    def __init__(self, file: File):
        self.file:File = file

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
        self.recordId:int = recordId
        self.fieldId:int = fieldId
        self.notes:str = notes
        self.modifiedDate:datetime = modifiedDate
        self.fileName:str = fileName
        self.filePath:str = filePath
        self.contentType:str = contentType

class SaveFileResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to save a file in Onspring.

    Attributes:
        id (`int`): The id of the file saved in Onspring.
    """

    def __init__(self, id: int):
        self.id:int = id

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

    def __init__(self, listId: int, name: str, id: uuid.UUID=None, numericValue: int=None, color: str=None):
        self.listId:int = listId
        self.name:str = name
        self.id:uuid.UUID = id
        self.numericValue:int = numericValue
        self.color:str = color

class AddOrUpdateListItemResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to add or update a list value in Onspring.

    Attributes:
        id (`int`): The id of the list value updated or added in Onspring.
    """

    def __init__(self, id: uuid.UUID):
        self.id:uuid.UUID = id

# record specific

class TimeSpanData:
    """
    An object to represent the data that makes up an Onspring timespan field.

    Attributes:
        quantity (`Decimal`):
        increment (`Enums.Increment`):
        recurrence (`Enums.Recurrence`):
        endByDate (`datetime`):
        endAfterOccurrences (`int`):
    """

    def __init__(self, quantity: Decimal, increment: Increment, recurrence: Recurrence=None, endByDate: datetime=None, endAfterOccurrences: int=None):
        self.quantity:Decimal = quantity
        self.increment:Increment = increment
        self.recurrence:Recurrence = recurrence
        self.endByDate:datetime = endByDate
        self.endAfterOccurrences:int = endAfterOccurrences

    def AsString(self) -> str:
        if self.endByDate != None:
            formattedDate = self.endByDate.strftime("%m/%d/%Y %I:%M %p")
            return f'Every {self.quantity} {self.increment} End By {formattedDate}'
        elif self.endAfterOccurrences != None:
            return f'Every {self.quantity} {self.increment} End After {self.endAfterOccurrences}'
        else:
            return f'{self.quantity} {self.increment}'

class Attachment:
    """
    An object to represent an attachment in Onspring.

    Attributes:
        fileId (`int`): The id of the file in Onspring.
        fileName (`str`): The name of the file in Onspring.
        notes (`str`): The notes for the file in Onspring.
        storageLocation (`str`): The storage location of the file in Onspring.
    """

    def __init__(self, fileId: int, fileName: str, notes: str, storageLocation: str):
        self.fileId:int = fileId
        self.fileName:str = fileName
        self.notes:str = notes
        self.storageLocation:str = storageLocation

class ScoringGroup:
    """
    An object to represent an Onspring scoring group.

    Attributes:
        listValueId (`UUID`): The id of the list value.
        name (`str`): The name of the list value.
        score (`Decimal`): The score for the list value.
        maximumScore (`Decimal`): The maximum possible score for the group.
    """

    def __init__(self, listValueId: uuid.UUID, name: str, score: Decimal, maximumScore: Decimal):
        self.listValueId:uuid.UUID = listValueId
        self.name:str = name
        self.score:Decimal = score
        self.maximumScore:Decimal = maximumScore

class RecordFieldValue:
    """
    An object to represent the value in a field in an Onspring record.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`str`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value, type: str=None):
        self.fieldId:int = fieldId
        self.value = value
        self.type:str = type

    def AsString(self) -> str | None:
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

    def AsInteger(self) -> int | None:
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

    def AsDecimal(self) -> Decimal | None:
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

    def AsDate(self) -> datetime | None:
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

    def AsGuid(self) -> uuid.UUID | None:
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
        
    def AsTimeSpan(self) -> TimeSpanData | None:
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

    def AsStringList(self) -> list[str] | None:
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

    def AsIntegerList(self) -> list[int] | None:
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

    def AsGuidList(self) -> list[uuid.UUID] | None:
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

    def AsAttachmentList(self) -> list[Attachment] | None:
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

    def AsScoringGroupList(self) -> list[ScoringGroup] | None:
        """
        If the `Models.RecordFieldValue` type is ScoringGroupList will return the value property as a `list[Models.ScoringGroup]` otherwise will return `None`.

        Args:
            None

        Returns:
            The value of the `Models.RecordFieldValue` as a `list[Models.ScoringGroup]`.
        """

        if self.type != ResultValueType.ScoringGroupList.name:
            return None

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

    def AsFileList(self) -> list[int] | None:
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

    def getValue(self) -> object:
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

    def GetResultValueString(self) -> str:
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
        self.appId:int = appId
        self.recordId:recordId = recordId
        self.fields:list[RecordFieldValue] = fields

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
        self.appId:int = appId
        self.fieldIds:list[int] = fieldIds
        self.dataFormat:str = dataFormat
        self.pageSize:int = pagingRequest.pageSize
        self.pageNumber:int = pagingRequest.pageNumber

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
        self.appId:int = appId
        self.filter:str = filter
        self.fieldIds:list[int] = fieldIds
        self.dataFormat:str = dataFormat
        self.pagingRequest:PagingRequest = pagingRequest

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
        self.pageNumber:int = pageNumber
        self.pageSize:int = pageSize
        self.totalPages:int = totalPages
        self.totalRecords:int = totalRecords
        self.records:list[Record] = records

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
        self.appId:int = appId
        self.recordId:int = recordId
        self.fieldIds:list[int] = fieldIds
        self.dataFormat:str = dataFormat

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
        self.appId:int = appId
        self.recordIds:list[int] = recordIds
        self.fieldIds:list[int] = fieldIds
        self.dataFormat:str = dataFormat

class GetBatchRecordsResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to request a batch of Onspring records.

    Attributes:
        count (`int`): The number of records requested.
        records (`list[Models.Record]`): The records requested.
    """

    def __init__(self, count: int, records: list[Record]):
        self.count:int = count
        self.records:list[Record] = records

class AddOrUpdateRecordResponse:
    """
    An object to represent a response to a request made by an `OnspringClient` to add or update an Onspring record.
    
    Attributes:
        id (`int`): The id of the Onspring record that was added or updated.
        warnings ('list[str]'): A list of warnings.
    """

    def __init__(self, id: int, warnings: list[str]=[]):
        self.id:int = id
        self.warnings:list[str] = warnings

class DeleteBatchRecordsRequest:
    """
    An object to represent all the necessary information for making a succcessful request to delete a batch of Onspring records by their ids.

    Attributes:
        appId (`int`): The id for the Onspring app where the records reside.
        recordId (`list[int]`): The ids for the records being deleted.
    """

    def __init__(self, appId: int, recordIds: list[int]):
        self.appId:int = appId
        self.recordIds:list[int] = recordIds

# field types

class StringFieldValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the String type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`str`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value):
        self.type:str = ResultValueType.String.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class IntegerFieldValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the Integer type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`int`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: int):
        self.type:str = ResultValueType.Integer.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class DecimalFieldValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the Decimal type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`Decimal`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: Decimal):
        self.type:str = ResultValueType.Decimal.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class DateFieldValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the Date type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`datetime`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: datetime):
        self.type:str = ResultValueType.Date.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class GuidFieldValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the Guid type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`UUID`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: uuid.UUID):
        self.type:str = ResultValueType.Guid.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class TimeSpanValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the TimeSpan type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`Models.TimeSpanData`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: TimeSpanData):
        self.type:str = ResultValueType.TimeSpan.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class StringListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the StringList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[str]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[str]):
        self.type:str = ResultValueType.StringList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class IntegerListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the IntegerList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[int]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[int]):
        self.type:str = ResultValueType.IntegerList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class GuidListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the GuidList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[UUID]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[uuid.UUID]):
        self.type:str = ResultValueType.GuidList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class AttachmentListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the AttachmentList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[Models.Attachment]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[Attachment]):
        self.type:str = ResultValueType.AttachmentList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class FileListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the FileList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[int]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[int]):
        self.type:str = ResultValueType.FileList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

class ScoringGroupListValue(RecordFieldValue):
    """
    An object to represent an Onspring field value of the ScoringGroupList type.

    Attributes:
        fieldId (`int`): The id of the field that the value is in.
        value (`list[Models.ScoringGroup]`): The value of the field.
        type (`str`): The type of value.
    """

    def __init__(self, fieldId: int, value: list[ScoringGroup]):
        self.type:str = ResultValueType.ScoringGroupList.name
        RecordFieldValue.__init__(self, fieldId, value, self.type)

# report specific

class GetReportByIdRequest:
    """
    An object to represent the necessary information to make a successful request to get a report by it's id.

    Attributes:
        reportId (`int`): The id of the report.
        apiDataFormat (`str`): The format of the data in the report.
        dataType (`str`): The data type for the report.
    """
    
    def __init__(self, reportId: int, apiDataFormat: str=DataFormat.Raw.name, dataType: str=ReportDataType.ReportData.name):
        self.reportId:int = reportId
        self.apiDataFormat:str = apiDataFormat
        self.dataType:str = dataType

class Row:
    """
    An object to represent a row of an Onspring report.
    
    Attributes:
        recordId (`int`): The id of the record who's data is held in the row.
        cells (`list[str]`): The record field values held in the row.
    """

    def __init__(self, recordId: int, cells: list[str]):
        self.recordId:int = recordId
        self.cells:list[str] = cells

class GetReportByIdResponse:
    """
    An object to represent the response to a request made by an `OnspringClient` to get a report by its id.

    Attributes:
        columns (`list[int]`): Values indicating the columns in the report.
        rows (`list[Models.Row]`): A collection of rows representing the records in the report.
    """

    def __init__(self, columns: list[str], rows: list[Row]):
        self.columns:list[str] = columns
        self.rows:list[Row] = rows

class Report:
    """
    An object to represent an Onspring report.

    Attributes:
        appId (`int`): The id of the app the report resides in.
        id (`int`): The id of the report.
        name (`str`): The name of the report.
        description (`str`): The description for the report.
    """

    def __init__(self, appId: int, id: int, name: str, description: str):
        self.appId:int = appId
        self.id:int = id
        self.name:str = name
        self.description:str = description

class GetReportsByAppIdResponse:
    """
    An object to represent the response to a request made by an `OnspringClient` to get a collection of reports by an app id.

    Attributes:
        pageNumber (`int`): The page number returned.
        pageSize (`int`): The size of the page returned.
        totalPages (`int`): The total number of pages for the request.
        totalRecords (`int`): The total records for the request.
        reports (`list[Models.Report]`): The requested reports for the current page.
    """

    def __init__(self, pageNumber: int, pageSize: int, totalPages: int, totalRecords: int, reports: list[Report]):
        self.pageNumber:int = pageNumber
        self.pageSize:int = pageSize
        self.totalPages:int = totalPages
        self.totalRecords:int = totalRecords
        self.reports:list[Report] = reports

# generic

class ApiResponse:
    """
    An object to represent a response to a request made by an `OnspringClient`.

    Attributes:
        statusCode (`int`): The http status code of the response.
        data: If the request was successful will contain the response data deserialized to custom python objects.
        message (`str`): A message that may provide more detail about the requests success or failure.
        raw (`requests.Response`): Exposes the raw response object of the request if you'd like to handle it directly.
    """

    def __init__(
        self, 
        statusCode:int=None, 
        data:
        GetAppsResponse|
        GetAppByIdResponse|
        GetAppsByIdsResponse|
        GetFieldByIdResponse|
        GetFieldsByIdsResponse|
        GetFieldsByAppIdResponse|
        GetFileInfoByIdResponse|
        GetFileByIdResponse|
        SaveFileResponse|
        AddOrUpdateListItemResponse|
        GetRecordsResponse|
        Record|
        GetBatchRecordsResponse|
        AddOrUpdateRecordResponse|
        GetReportByIdResponse|
        GetReportsByAppIdResponse=None,
        message:str=None, 
        raw:Response=None
        ):
        self.statusCode:int = statusCode
        self.isSuccessful:bool = int(statusCode) < 400
        self.data = data
        self.message:str = message
        self.raw:Response = raw