import requests
import json
import re

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
                message='Invalid paging information',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

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
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    def GetAppById(self, appId: int):

        endpoint = GetAppByIdEndpoint(self.baseUrl, appId)

        response = requests.request(
            'GET',
            endpoint,
            headers=self.headers)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='App could not be found',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

            responseJson = response.json()

            app = App(
                responseJson['href'],
                responseJson['id'],
                responseJson['name'])

            data = GetAppByIdResponse(app)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

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
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

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
                apps)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

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
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='Field could not be found',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

            jsonResponse = response.json()

            field = Field(
                jsonResponse['id'],
                jsonResponse['appId'],
                jsonResponse['name'],
                jsonResponse['type'],
                jsonResponse['status'],
                jsonResponse['isRequired'],
                jsonResponse['isUnique'],)

            data = GetFieldByIdResponse(field)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

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
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field(s)',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='Field(s) could not be found',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

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
                fields)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

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
                message='Invalid paging information',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

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
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    # file methods

    def GetFileInfoById(self, recordId: int, fieldId: int, fileId: int):

        endpoint = GetFileInfoByIdEndpoint(
            self.baseUrl,
            recordId,
            fieldId,
            fileId)

        response = requests.request(
            'GET',
            endpoint,
            headers=self.headers,)

        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Request is invalid based on underlying data',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403:
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the file',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 404:
            return ApiResponse(
                response.status_code,
                message='File could not be found',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:

            jsonResponse = response.json()

            fileInfo = FileInfo(
                jsonResponse["type"],
                jsonResponse["contentType"],
                jsonResponse["name"],
                jsonResponse["createdDate"],
                jsonResponse["modifiedDate"],
                jsonResponse["owner"],
                jsonResponse["fileHref"])

            data = GetFileInfoByIdResponse(fileInfo)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    def DeleteFileById(self, recordId: int, fieldId: int, fileId: int):

        endpoint = DeleteFileByIdEndpoint(
            self.baseUrl,
            recordId,
            fieldId,
            fileId)

        response = requests.request(
            'DELETE',
            endpoint,
            headers=self.headers,)

        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Request is invalid based on underlying data',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403 or response.status_code == 404:

            jsonResponse = response.json()

            return ApiResponse(
                response.status_code,
                message=jsonResponse["message"],
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 500:
            return ApiResponse(
                response.status_code,
                message='File could not be deleted due to internal error',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 204:
            return ApiResponse(
                response.status_code,
                message="File deleted successfully",
                headers=response.headers,
                responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    def GetFileById(self, recordId: int, fieldId: int, fileId: int):

        endpoint = GetFileByIdEndpoint(
            self.baseUrl,
            recordId,
            fieldId,
            fileId)

        response = requests.request(
            'GET',
            endpoint,
            headers=self.headers,)

        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Request is invalid based on underlying data',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 403 or response.status_code == 404:
            
            jsonResponse = response.json()

            return ApiResponse(
                response.status_code,
                message=jsonResponse["message"],
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 200:
            
            fileName = response.headers["Content-Disposition"]
            result = re.search("filename=.*;", fileName).group()

            if result:
                fileName = re.sub("filename=|\"|;", "", result)
            else:
                fileName = None

            file = File(
                fileName,
                response.headers["Content-Type"],
                response.headers["Content-Length"],
                response.content)

            data = GetFileByIdResponse(file)

            return ApiResponse(
                response.status_code,
                data,
                headers=response.headers,
                responseText=response.text)
        

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    def SaveFile(self,  saveFileRequest: SaveFileRequest):

        endpoint = SaveFileEndpoint(self.baseUrl)

        requestData = {
            "recordId": saveFileRequest.recordId,
            "fieldId": saveFileRequest.fieldId,
            "notes": saveFileRequest.notes,
            "modifiedDate": saveFileRequest.modifiedDate
        }

        files = [
            (
                'File',
                (saveFileRequest.fileName, open(saveFileRequest.filePath,'rb'),saveFileRequest.contentType)
            )
        ]

        response = requests.request(
            "POST", 
            endpoint, 
            headers=self.headers,
            data=requestData,
            files=files)


        if response.status_code == 400:
            return ApiResponse(
                response.status_code,
                message='Request is invalid based on underlying data',
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                headers=response.headers,
                responseText=response.text)

        if response.status_code in [403,404,500]:

            jsonResponse = response.json()

            return ApiResponse(
                response.status_code,
                message=jsonResponse["message"],
                headers=response.headers,
                responseText=response.text)

        if response.status_code == 201:
            responseJson = response.json()

            data = SaveFileResponse(responseJson["id"])

            return ApiResponse(
                    response.status_code,
                    data,
                    headers=response.headers,
                    responseText=response.text)

        return ApiResponse(
            response.status_code,
            headers=response.headers,
            responseText=response.text)

    # list methods
    # record methods
    # report methods