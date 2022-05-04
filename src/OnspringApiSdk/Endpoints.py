import uuid

# connectivity endpoints

def GetPingEndpoint(baseUrl: str):
    """
    Returns the ping endpoint.

    Args:
        baseUrl (`str`): The base url for the api.

    Returns:
        The ping endpoint as a string.
    """
    
    return f'{baseUrl}/Ping'

# app endpoints

def GetAppsEndpoint(baseUrl: str):
    """
    Returns the get apps endpoint.

    Args:
        baseUrl (`str`): The base url for the api.

    Returns:
        The get apps endpoint as a string.
    """

    return f'{baseUrl}/Apps'

def GetAppByIdEndpoint(baseUrl: str, appId: int):
    """
    Returns the get app by id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app being requested.

    Returns:
        The get app by id endpoint as a string.
    """

    return f'{baseUrl}/Apps/id/{appId}'

def GetAppsByIdsEndpoint(baseUrl: str):
    """
    Returns the get apps by ids endpoint.

    Args:
        baseUrl (`str`): The base url for the api.

    Returns:
        The get apps by ids endpoint as a string.
    """

    return f'{baseUrl}/Apps/batch-get'

# field endpoints

def GetFieldByIdEndpoint(baseUrl: str, fieldId: int):
    """
    Returns the get field by id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        fieldId (`int`): The id of the field being requested.

    Returns:
        The get field by id endpoint as a string.
    """

    return f'{baseUrl}/Fields/id/{fieldId}'

def GetFieldsByIdsEndpoint(baseUrl: str):
    """
    Returns the get fields by ids endpoint.

    Args:
        baseUrl (`str`): The base url for the api.

    Returns:
        The get fields by ids endpoint as a string.
    """

    return f'{baseUrl}/Fields/batch-get'

def GetFieldsByAppIdEndpoint(baseUrl: str, appId: int):
    """
    Returns the get fields by app id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app whose fields are being requested.

    Returns:
        The get fields by app id endpoint as a string.
    """

    return f'{baseUrl}/Fields/appId/{appId}'

# file endpoints

def GetFileInfoByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    """
    Returns the get file info by its id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        recordId (`int`): The id for the record where the file resides.
        fieldId (`int`): The id for the field in the record where the file is held.
        fileId ('int'): The id of the file.

    Returns:
        The get file info by its id endpoint as a string.
    """

    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}'

def DeleteFileByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    """
    Returns the delete file by its id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        recordId (`int`): The id for the record where the file resides.
        fieldId (`int`): The id for the field in the record where the file is held.
        fileId ('int'): The id of the file.

    Returns:
        The delete file by its id endpoint as a string.
    """

    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}'

def GetFileByIdEndpoint(baseUrl: str, recordId: int, fieldId: int, fileId: int):
    """
    Returns the get file by its id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        recordId (`int`): The id for the record where the file resides.
        fieldId (`int`): The id for the field in the record where the file is held.
        fileId ('int'): The id of the file.

    Returns:
        The get file by its id endpoint as a string.
    """

    return f'{baseUrl}/Files/recordId/{recordId}/fieldId/{fieldId}/fileId/{fileId}/file'

def SaveFileEndpoint(baseUrl: str):
    """
    Returns the save file endpoint.

    Args:
        baseUrl (`str`): The base url for the api.

    Returns:
        The save file endpoint as a string.
    """

    return f'{baseUrl}/Files'

# list endpoints

def AddOrUpdateListItemEndpoint(baseUrl, listId: int):
    """
    Returns the add or update list item endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        listId (`int`): The id of the list for which the item belongs when being updated or being added to.

    Returns:
        The add or update list item endpoint as a string.
    """

    return f'{baseUrl}/Lists/id/{listId}/items'

def DeleteListItemEndpoint(baseUrl: str, listId: int, itemId: uuid):
    """
    Returns the delete list item endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        listId (`int`): The id of the list for which the list item belongs.
        itemId (`int`): The id list item.

    Returns:
        The delete list item endpoint as a string.
    """

    return f'{baseUrl}/Lists/id/{listId}/itemId/{itemId}'

# record endpoints

def GetRecordsByAppIdEndpoint(baseUrl, appId: int):
    """
    Returns the get records by app id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app where the records reside.
    
    Returns:
        The get records by app id endpoint as a string.
    """

    return f'{baseUrl}/Records/appId/{appId}'

def GetRecordByIdEndpoint(baseUrl, appId: int, recordId: int):
    """
    Returns the get record by id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app where the record resides.
        recordId (`int`): The id of the record.
    
    Returns:
        The get record by id endpoint as a string.
    """

    return f'{baseUrl}/Records/appId/{appId}/recordId/{recordId}'

def DeleteRecordByIdEndpoint(baseUrl, appId: int, recordId: int):
    """
    Returns the delete record by id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app where the record resides.
        recordId (`int`): The id of the record.
    
    Returns:
        The delete record by id endpoint as a string.
    """

    return f'{baseUrl}/Records/appId/{appId}/recordId/{recordId}'

def GetRecordsByIdsEndpoint(baseUrl):
    """
    Returns the get records by ids endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
    
    Returns:
        The get records by ids endpoint as a string.
    """
    
    return f'{baseUrl}/Records/batch-get'

def QueryRecordsEndpoint(baseUrl):
    """
    Returns the query records endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
    
    Returns:
        The query records endpoint as a string.
    """

    return f'{baseUrl}/Records/Query'

def AddOrUpdateRecordEndpoint(baseUrl):
    """
    Returns the add or update record endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
    
    Returns:
        The add or update record endpoint as a string.
    """

    return f'{baseUrl}/Records'

def DeleteRecordsByIds(baseUrl):
    """
    Returns the delete records by ids endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
    
    Returns:
        The delete records by ids endpoint as a string.
    """

    return f'{baseUrl}/Records/batch-delete'

# report endpoints

def GetReportByIdEndpoint(baseUrl, reportId: int):
    """
    Returns the get report by id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        reportId (`int`): The id of the report.
    
    Returns:
        The get report by id endpoint as a string.
    """

    return f'{baseUrl}/Reports/id/{reportId}'

def GetReportsByAppIdEndpoint(baseUrl, appId: int):
    """
    Returns the get reports by app id endpoint.

    Args:
        baseUrl (`str`): The base url for the api.
        appId (`int`): The id of the app where the reports reside.
    
    Returns:
        The get reports by app id endpoint as a string.
    """

    return f'{baseUrl}/Reports/appId/{appId}'