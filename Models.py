import datetime

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