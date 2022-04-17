import uuid

# connectivity endpoints

def GetPingEndpoint(baseUrl: str):
    return f'{baseUrl}/Ping'

# app endpoints

def GetAppsEndpoint(baseUrl: str):
    return f'{baseUrl}/Apps'

def GetAppByIdEndpoint(baseUrl: str, appId: int):
    return f'{baseUrl}/Apps/id/{appId}'

def GetAppByIdsEndpoint(baseUrl: str):
    return f'{baseUrl}/Apps/batch-get'

# field endpoints

def GetFieldByIdEndpoint(baseUrl: str, fieldId: int):
    return f'{baseUrl}/Fields/id/{fieldId}'

def GetFieldsByIdsEndpoint(baseUrl: str):
    return f'{baseUrl}/Fields/batch-get'

def GetFieldsByAppIdEndpoint(baseUrl: str, appId: int):
    return f'{baseUrl}/Fields/appId/{appId}'

# file endpoints

def GetFileInfoByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}'

def DeleteFileByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}'

def GetFileByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}/file'

def SaveFileEndpoint(baseUrl: str):
    return f'{baseUrl}/Files'

# list endpoints

def AddOrUpdateListItemEndpoint(baseUrl, listId: int):
    return f'{baseUrl}/Lists/id/{listId}/items'

def DeleteListItemEndpoint(baseUrl: str, listId: int, itemId: uuid):
    return f'{baseUrl}/Lists/id/{listId}/itemId/{itemId}'

# record endpoints

def GetRecordsByAppIdEndpoint(baseUrl, appId: int):
    return f'{baseUrl}/Records/appId/{appId}'

def GetRecordByIdEndpoint(baseUrl, appId: int, recordId: int):
    return f'{baseUrl}/Records/appId/{appId}/recordId/{recordId}'

def DeleteRecordByIdEndpoint(baseUrl, appId: int, recordId: int):
    return f'{baseUrl}/Records/appId/{appId}/recordId/{recordId}'

def GetRecordsByIdsEndpoint(baseUrl):
    return f'{baseUrl}/Records/batch-get'

def QueryRecordsEndpoint(baseUrl):
    return f'{baseUrl}/Records/Query'

def AddOrUpdateRecordEndpoint(baseUrl):
    return f'{baseUrl}/Records'

def DeleteRecordsByIds(baseUrl):
    return f'{baseUrl}/Records/batch-delete'

# report endpoints

def GetReportByIdEndpoint(baseUrl, reportId: int):
    return f'{baseUrl}/Reports/id/{reportId}'

def GetReportsByAppIdEndpoint(baseUrl, appId: int):
    return f'{baseUrl}/Reports/appId/{appId}'