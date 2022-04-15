# connectivity endpoints

def GetPingEndpoint(baseUrl):
    return f'{baseUrl}/Ping'

# app endpoints

def GetAppsEndpoint(baseUrl):
    return f'{baseUrl}/Apps'

def GetAppByIdEndpoint(baseUrl, appId):
    return f'{baseUrl}/Apps/id/{appId}'

def GetAppByIdsEndpoint(baseUrl):
    return f'{baseUrl}/Apps/batch-get'

# field endpoints

def GetFieldByIdEndpoint(baseUrl, fieldId):
    return f'{baseUrl}/Fields/id/{fieldId}'

def GetFieldsByIdsEndpoint(baseUrl):
    return f'{baseUrl}/Fields/batch-get'

def GetFieldsByAppIdEndpoint(baseUrl, appId):
    return f'{baseUrl}/Fields/appId/{appId}'

# file endpoints

# list endpoints

# record endpoints

# report endpoints