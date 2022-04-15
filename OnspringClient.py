import requests
import json

from UrlHelper import *
from Models import *


class OnspringClient:
    def __init__(self, url, key):
        self.baseUrl = url
        self.headers = {
            'x-apikey': key,
            'x-api-version': '2'
        }

    # connectivity methods

    def canConnect(self):

        endpoint = GetPingEndpoint(self.baseUrl)

        response = requests.request(
            'GET', 
            endpoint, 
            headers=self.headers)

        return response.status_code == 200

    # app methods

    def GetApps(self, pagingRequest=PagingRequest(1, 50)):

        endpoint = GetAppsEndpoint(self.baseUrl)

        params = pagingRequest.__dict__

        response = requests.request(
            'GET', 
            endpoint, 
            headers=self.headers, 
            params=params)

        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Invalid paging information')

        if response.status_code == 401:
            return ApiResponse(
                response.status_code, 
                message='Unauthorized request')

        responseJson = response.json()

        apps = []

        for item in responseJson['items']:
            app = App(
                item['href'], 
                item['id'], 
                item['name'])
            
            apps.append(app)

        data = GetAppsResponse(
            responseJson['pageNumber'], 
            responseJson['pageSize'], 
            responseJson['totalPages'], 
            responseJson['totalRecords'], 
            apps)

        return ApiResponse(
            response.status_code, 
            data)

    def GetAppById(self, appId: int):

        endpoint = GetAppByIdEndpoint(self.baseUrl, appId)

        response = requests.request(
            'GET', 
            endpoint, 
            headers=self.headers)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request'
            )

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app'
            )

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='App could not be found'
            )
        
        responseJson = response.json()

        app = App(
            responseJson['href'],
            responseJson['id'],
            responseJson['name'])

        data = GetAppByIdResponse(app)

        return ApiResponse(
            response.status_code,
            data
        )

    def GetAppByIds(self, appIds: list):

        endpoint = GetAppByIdsEndpoint(self.baseUrl)

        self.headers['Content-Type'] = 'application/json'

        # make sure appIds can be serialized to json string
        if not isinstance(appIds, (list, tuple)):
            return ApiResponse(
                400,
                message='App ids should be of type list or tuple')

        appIds = json.dumps(appIds)

        response = requests.request(
            'POST', 
            endpoint, 
            headers=self.headers, 
            data=appIds)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request'
            )

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app'
            )

        responseJson = response.json()

        apps = []

        for item in responseJson['items']:
            app = App(
                item['href'], 
                item['id'], 
                item['name'])
            
            apps.append(app)

        data = GetAppsByIdsResponse(
            responseJson['count'],
            apps
        )

        return ApiResponse(
            response.status_code,
            data
        )

    # field methods

    def GetFieldById(self, fieldId: int):

        endpoint = GetFieldByIdEndpoint(self.baseUrl, fieldId)

        response = requests.request(
            'GET', 
            endpoint, 
            headers=self.headers)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request'
            )

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field'
            )

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='Field could not be found'
            )
        
        jsonResponse = response.json()

        field = Field(
            jsonResponse['id'],
            jsonResponse['appId'],
            jsonResponse['name'],
            jsonResponse['type'],
            jsonResponse['status'],
            jsonResponse['isRequired'],
            jsonResponse['isUnique'],
        )

        data = GetFieldByIdResponse(field)

        return ApiResponse(
            response.status_code,
            data
        )

    def GetFieldsByIds(self, fieldIds: list):

        endpoint = GetFieldsByIdsEndpoint(self.baseUrl)

        self.headers['Content-Type'] = 'application/json'

        # make sure fieldIds can be serialized to json string
        if not isinstance(fieldIds, (list, tuple)):
            return ApiResponse(
                400,
                message='Field ids should be of type list or tuple')

        fieldIds = json.dumps(fieldIds)

        response = requests.request(
            'POST', 
            endpoint, 
            headers=self.headers, 
            data=fieldIds)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request'
            )

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field(s)'
            )

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='Field(s) could not be found'
            )

        responseJson = response.json()

        fields = []

        for item in responseJson['items']:
            field = Field(
                item['id'], 
                item['appId'], 
                item['name'],
                item['type'],
                item['status'],
                item['isRequired'],
                item['isUnique'])
            
            fields.append(field)

        data = GetFieldsByIdsResponse(
            responseJson['count'],
            fields
        )

        return ApiResponse(
            response.status_code,
            data
        )

    def GetFieldsByAppId(self, appId: int, pagingRequest=PagingRequest(1, 50)):

        endpoint = GetFieldsByAppIdEndpoint(self.baseUrl, appId)

        params = pagingRequest.__dict__

        response = requests.request(
            'GET', 
            endpoint, 
            headers=self.headers, 
            params=params)

        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Invalid paging information')

        if response.status_code == 401:
            return ApiResponse(
                response.status_code, 
                message='Unauthorized request')

        responseJson = response.json()

        fields = []

        for item in responseJson['items']:
            field = Field(
                item['id'], 
                item['appId'], 
                item['name'],
                item['type'],
                item['status'],
                item['isRequired'],
                item['isUnique'])
            
            fields.append(field)

        data = GetFieldsByAppIdResponse(
            responseJson['pageNumber'], 
            responseJson['pageSize'], 
            responseJson['totalPages'], 
            responseJson['totalRecords'], 
            fields)

        return ApiResponse(
            response.status_code, 
            data)

    # file methods

    # list methods

    # record methods

    # report methods

url = 'https://api.onspring.com'
apiKey = '61642d8c686f9e8747e42af8/52cae9a9-4c49-48b6-a3fe-10a48d46ac69'

onspringClient = OnspringClient(url, apiKey)

response = onspringClient.GetFieldsByAppId(8)

print()
