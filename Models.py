class ApiResponse:
    def __init__(self, statusCode=None, data=None, message=None):
        self.statusCode = statusCode
        self.isSuccessful = int(statusCode) < 400
        self.data = data
        self.message = message

class PagingRequest:
    def __init__(self, pageNumber, pageSize):
        self.pageNumber = pageNumber
        self.pageSize = pageSize

class App:
    def __init__(self, href, id, name):
        self.href = href
        self.id = id
        self.name = name

class GetAppsResponse:
    def __init__(self, pageNumber, pageSize, totalPages, totalRecords, apps: list[App]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.apps = apps

class GetAppByIdResponse:
    def __init__(self, app: App):
        self.app = app

class GetAppsByIdsResponse:
    def __init__(self, count, apps: list[App]):
        self.count = count
        self.apps = apps

class Field:
    def __init__(self, id, appId, name, type, status, isRequired, isUnique):
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
    def __init__(self, count, fields: list[Field]):
        self.count = count
        self.fields = fields

class GetFieldsByAppIdResponse:
    def __init__(self, pageNumber, pageSize, totalPages, totalRecords, fields: list[Field]):
        self.pageNumber = pageNumber
        self.pageSize = pageSize
        self.totalPages = totalPages
        self.totalRecords = totalRecords
        self.fields = fields