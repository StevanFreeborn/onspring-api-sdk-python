import requests
import json
from UrlHelper import *

class OnspringClient:
    def __init__(self, url, key):
        self.baseUrl = url
        self.headers = {
            'x-apikey': key,
            'x-api-version': '2'
        }
    
    # verify connectivity 

    def canConnect(self):
        
        endpoint = GetPingEndpoint(self.baseUrl)

        response = requests.request('GET', endpoint, headers=self.headers)

        return response.status_code == 200

    # apps

    def GetApps(self, pageNumber=1, pageSize=50):
        
        endpoint = GetAppsEndpoint(self.baseUrl)

        params={
            'PageNumber': pageNumber,
            'PageSize': pageSize
        }

        response = requests.request('GET', endpoint, headers=self.headers, params=params)

        if(response.status_code == 400):
            return {'Message': 'Invalid paging information.'}
        
        if(response.status_code == 401):
            return {'Message': 'Unauthorized request.'}

        return response.json()

    def GetAppById(self, appId):
        
        endpoint = GetAppByIdEndpoint(self.baseUrl, appId)

        response = requests.request('GET', endpoint, headers=self.headers)

        if(response.status_code == 401):
            return {'Message': 'Unauthorized request.'}
        
        if(response.status_code == 403):
            return {'Message': 'Client does not have read access to the app.'}
        
        if(response.status_code == 404):
            return {'Message': 'App could not be found.'}

        return response.json()

    def GetAppByIds(self, appIds):
        
        endpoint = GetAppByIdsEndpoint(self.baseUrl)

        self.headers["Content-Type"] = "application/json"
        
        if(not isinstance(appIds, (list, tuple))):
            return {'Message': 'App ids should be of type list or tuple.'}
    
        data = json.dumps(appIds)

        response = requests.request("POST", endpoint, headers=self.headers, data=data)

        if(response.status_code == 401):
            return {'Message': 'Unauthorized request.'}
        
        if(response.status_code == 403):
            return {'Message': 'Client does not have read access to the app.'}

        return response.json()


        
url = 'https://api.onspring.com'
apiKey = '61642d8c686f9e8747e42af8/52cae9a9-4c49-48b6-a3fe-10a48d46ac69'

onspringClient = OnspringClient(url,apiKey)

data = (8,)

print(onspringClient.GetAppByIds(data))