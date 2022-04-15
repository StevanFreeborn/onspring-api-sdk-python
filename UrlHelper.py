def GetPingEndpoint(baseUrl):
    return f'{baseUrl}/Ping'

def GetAppsEndpoint(baseUrl):
    return f'{baseUrl}/Apps'

def GetAppByIdEndpoint(baseUrl, appId):
    return f'{baseUrl}/Apps/id/{appId}'

def GetAppByIdsEndpoint(baseUrl):
    return f'{baseUrl}/Apps/batch-get'