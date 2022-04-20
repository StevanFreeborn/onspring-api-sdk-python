import requests
import json
import re

from Endpoints import *
from Models import *

class OnspringClient:
    def __init__(self, url, key):
        self.baseUrl = url
        self.headers = {
            'x-apikey': key,
            'x-api-version': '2'
        }

    # connectivity methods

    def CanConnect(self):

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
                raw=response)

        if response.status_code == 401:
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 200:

            responseJson = dict(response.json())

            apps = []

            for item in responseJson.get('items'):

                item = dict(item)

                app = App(
                    item.get('href'),
                    item.get('id'),
                    item.get('name'))

                apps.append(app)

            data = GetAppsResponse(
                responseJson.get('pageNumber'),
                responseJson.get('pageSize'),
                responseJson.get('totalPages'),
                responseJson.get('totalRecords'),
                apps)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 403:
            
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app',
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='App could not be found',
                raw=response)

        if response.status_code == 200:

            responseJson = dict(response.json())

            app = App(
                responseJson.get('href'),
                responseJson.get('id'),
                responseJson.get('name'))

            data = GetAppByIdResponse(app)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    def GetAppsByIds(self, appIds: list):

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
                raw=response)

        if response.status_code == 403:
            
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the app',
                raw=response)

        if response.status_code == 200:

            responseJson = dict(response.json())

            apps = []

            for item in responseJson['items']:

                item = dict(item)

                app = App(
                    item.get('href'),
                    item.get('id'),
                    item.get('name'))

                apps.append(app)

            data = GetAppsByIdsResponse(
                responseJson.get('count'),
                apps)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 403:
            
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field',
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='Field could not be found',
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            field = Field(
                jsonResponse.get('id'),
                jsonResponse.get('appId'),
                jsonResponse.get('name'),
                jsonResponse.get('type'),
                jsonResponse.get('status'),
                jsonResponse.get('isRequired'),
                jsonResponse.get('isUnique'))

            data = GetFieldByIdResponse(field)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 403:
            
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the field(s)',
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='Field(s) could not be found',
                raw=response)

        if response.status_code == 200:

            responseJson = dict(response.json())

            fields = []

            for item in responseJson.get('items'):
                
                item = dict(item)
                
                field = Field(
                    item.get('id'),
                    item.get('appId'),
                    item.get('name'),
                    item.get('type'),
                    item.get('status'),
                    item.get('isRequired'),
                    item.get('isUnique'))

                fields.append(field)

            data = GetFieldsByIdsResponse(
                responseJson.get('count'),
                fields)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 200:

            responseJson = dict(response.json())

            fields = []

            for item in responseJson.get('items'):

                item = dict(item)

                field = Field(
                    item.get('id'),
                    item.get('appId'),
                    item.get('name'),
                    item.get('type'),
                    item.get('status'),
                    item.get('isRequired'),
                    item.get('isUnique'))

                fields.append(field)

            data = GetFieldsByAppIdResponse(
                responseJson.get('pageNumber'),
                responseJson.get('pageSize'),
                responseJson.get('totalPages'),
                responseJson.get('totalRecords'),
                fields)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:
            
            return ApiResponse(
                response.status_code,
                message='Client does not have read access to the file',
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='File could not be found',
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            createdDate = parseDate(jsonResponse.get('createdDate'))
            modifiedDate = parseDate(jsonResponse.get('modifiedDate'))

            fileInfo = FileInfo(
                jsonResponse.get('type'),
                jsonResponse.get('contentType'),
                jsonResponse.get('name'),
                createdDate,
                modifiedDate,
                jsonResponse.get('owner'),
                jsonResponse.get('fileHref'))

            data = GetFileInfoByIdResponse(fileInfo)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403 or response.status_code == 404:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 500:
            
            return ApiResponse(
                response.status_code,
                message='File could not be deleted due to internal error',
                raw=response)

        if response.status_code == 204:
            
            return ApiResponse(
                response.status_code,
                message='File deleted successfully',
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

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
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403 or response.status_code == 404:
            
            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 200:

            headers = dict(response.headers)
            
            fileName = headers.get('Content-Disposition')
            result = re.search('filename=.*;', fileName).group()
            
            # TODO: implement attempting to build file name using content-type header
            # TODO: implement default filename value
            if result:
                fileName = re.sub('filename=|\'|;', '', result)
            else:
                fileName = 'OnspringFile'

            file = File(
                fileName,
                headers.get('Content-Type'),
                headers.get('Content-Length'),
                response.content)

            data = GetFileByIdResponse(file)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)
        

        return ApiResponse(
            response.status_code,
            raw=response)

    def SaveFile(self,  saveFileRequest: SaveFileRequest):

        endpoint = SaveFileEndpoint(self.baseUrl)

        files = [
            (
                'File',
                (saveFileRequest.fileName, open(saveFileRequest.filePath,'rb'),saveFileRequest.contentType)
            )
        ]

        saveFileRequest = saveFileRequest.__dict__
        del saveFileRequest['fileName']
        del saveFileRequest['filePath']
        del saveFileRequest['contentType']

        requestData = saveFileRequest

        response = requests.request(
            'POST', 
            endpoint, 
            headers=self.headers,
            data=requestData,
            files=files)

        if response.status_code == 400:
            
            return ApiResponse(
                response.status_code,
                message='Request is invalid based on underlying data',
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code in [403,404,500]:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 201:

            responseJson = dict(response.json())

            data = SaveFileResponse(responseJson.get('id'))

            return ApiResponse(
                    response.status_code,
                    data,
                    raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    # list methods

    def AddOrUpdateListItem(self, listItemRequest: ListItemRequest):

        endpoint = AddOrUpdateListItemEndpoint(self.baseUrl, listItemRequest.listId)

        self.headers['Content-Type'] = 'application/json'

        del listItemRequest.__dict__['listId']

        requestData = json.dumps(listItemRequest.__dict__)

        response = requests.request(
            'PUT', 
            endpoint, 
            headers=self.headers,
            data=requestData)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code in [403,404]:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 201:
            
            responseJson = dict(response.json())

            data = AddOrUpdateListItemResponse(responseJson.get('id'))

            return ApiResponse(
                    response.status_code,
                    data,
                    message='New list value successfully added',
                    raw=response)

        if response.status_code == 200:
            
            responseJson = dict(response.json())

            data = AddOrUpdateListItemResponse(responseJson.get('id'))

            return ApiResponse(
                    response.status_code,
                    data,
                    message='Existing list value successfully updated',
                    raw=response)
        
        return ApiResponse(
            response.status_code,
            raw=response)

    def DeleteListItem(self, listId: int, itemId: uuid):

        endpoint = DeleteListItemEndpoint(self.baseUrl, listId, itemId)

        response = requests.request(
            'DELETE',
            endpoint,
            headers=self.headers)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='List/item could not be found',
                raw=response)

        if response.status_code == 204:
            
            return ApiResponse(
                response.status_code,
                message='Item deleted successfully',
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    # record methods

    def GetRecordsByAppId(self, getRecordsByAppRequest: GetRecordsByAppRequest):

        endpoint = GetRecordsByAppIdEndpoint(self.baseUrl, getRecordsByAppRequest.appId)

        params = getRecordsByAppRequest.__dict__
        del params['appId']
        params['fieldIds'] = ",".join([str(i) for i in params['fieldIds']])

        response = requests.request(
            'GET',
            endpoint,
            headers=self.headers,
            params=params)

        if response.status_code == 400:
            
            return ApiResponse(
                response.status_code,
                message='Invalid paging information/size of the data requested was too large.',
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            records = []

            for item in jsonResponse.get('items'):
                
                item = dict(item)

                fields = []

                record = Record(
                    item.get('appId'),
                    fields,
                    item.get('recordId'))

                for field in item.get('fieldData'):
                    
                    field = dict(field)

                    field = RecordFieldValue(
                        field.get('fieldId'),
                        field.get('value'),
                        field.get('type'))
                    
                    fields.append(field)
            
                record.fields = fields

                records.append(record)

            data = GetRecordsResponse(
                jsonResponse.get('pageNumber'),
                jsonResponse.get('pageSize'),
                jsonResponse.get('totalPages'),
                jsonResponse.get('totalRecords'),
                records)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)
    
    def GetRecordById(self, getRecordByIdRequest: GetRecordByIdRequest):
        
        endpoint = GetRecordByIdEndpoint(self.baseUrl, getRecordByIdRequest.appId, getRecordByIdRequest.recordId)

        params = getRecordByIdRequest.__dict__
        del params['appId']
        del params['recordId']
        params['fieldIds'] = ",".join([str(i) for i in params['fieldIds']])

        response = requests.request(
            'GET', 
            endpoint,
            headers=self.headers, 
            params=params)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='Record could not be found',
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            fields = []

            for field in jsonResponse.get('fieldData'):
                    
                field = dict(field)

                field = RecordFieldValue(
                    field.get('fieldId'),
                    field.get('value'),
                    field.get('type'))
                    
                fields.append(field)

            data = Record(
                jsonResponse.get('appId'),
                fields,
                jsonResponse.get('recordId'))

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    def DeleteRecordById(self, appId: int, recordId: int):

        endpoint = DeleteRecordByIdEndpoint(self.baseUrl, appId, recordId)

        response = requests.request(
            'DELETE',
            endpoint,
            headers=self.headers)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 404:
            
            return ApiResponse(
                response.status_code,
                message='Record could not be found',
                raw=response)

        if response.status_code == 204:
            
            return ApiResponse(
                response.status_code,
                message='Record deleted successfully',
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)
        
    def GetRecordsByIds(self, getBatchRecordsRequest: GetBatchRecordsRequest):

        endpoint = GetRecordsByIdsEndpoint(self.baseUrl)

        self.headers['Content-Type'] = 'application/json'

        requestData = json.dumps(getBatchRecordsRequest.__dict__)

        response = requests.request(
            'POST',
            endpoint,
            headers=self.headers,
            data=requestData)

        if response.status_code == 400:
            
            return ApiResponse(
                response.status_code,
                message='Batch request is invalid/size of the data requested was too large.',
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            records = []

            for item in jsonResponse.get('items'):
                
                item = dict(item)

                fields = []

                record = Record(
                    item.get('appId'),
                    fields,
                    item.get('recordId'),)

                for field in item.get('fieldData'):
                    
                    field = dict(field)

                    field = RecordFieldValue(
                        field.get('fieldId'),
                        field.get('value'),
                        field.get('type'))
                    
                    fields.append(field)
            
                record.fields = fields

                records.append(record)

            data = GetBatchRecordsResponse(
                jsonResponse.get('count'),
                records)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    def QueryRecords(self, queryRecordsRequest: QueryRecordsRequest):

        endpoint = QueryRecordsEndpoint(self.baseUrl)
        
        self.headers['Content-Type'] = 'application/json'

        requestData = queryRecordsRequest.__dict__

        params = requestData.get('pagingRequest').__dict__

        del requestData['pagingRequest']

        requestData = json.dumps(requestData)

        response = requests.request(
            'POST',
            endpoint,
            headers=self.headers,
            data=requestData,
            params=params)

        if response.status_code == 400:
            
            return ApiResponse(
                response.status_code,
                message='Query request is invalid/size of the data requested was too large.',
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code == 403:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code == 200:

            jsonResponse = dict(response.json())

            records = []

            for item in jsonResponse.get('items'):
                
                item = dict(item)

                fields = []

                record = Record(
                    item.get('appId'),
                    fields,
                    item.get('recordId'))

                for field in item.get('fieldData'):
                    
                    field = dict(field)

                    field = RecordFieldValue(
                        field.get('fieldId'),
                        field.get('value'),
                        field.get('type'))
                    
                    fields.append(field)
            
                record.fields = fields

                records.append(record)

            data = GetRecordsResponse(
                jsonResponse.get('pageNumber'),
                jsonResponse.get('pageSize'),
                jsonResponse.get('totalPages'),
                jsonResponse.get('totalRecords'),
                records)

            return ApiResponse(
                response.status_code,
                data,
                raw=response)

        return ApiResponse(
            response.status_code,
            raw=response)

    def AddOrUpdateRecord(self, record: Record):

        endpoint = AddOrUpdateRecordEndpoint(self.baseUrl)

        self.headers['Content-Type'] = 'application/json'

        fieldsDict = {}

        for field in record.fields:
            fieldsDict[field.fieldId] = field.value

        record.fields = fieldsDict

        requestData = json.dumps(record.__dict__)

        response = requests.request(
            'PUT',
            endpoint,
            headers=self.headers,
            data=requestData)

        if response.status_code == 400:
            
            return ApiResponse(
                response.status_code,
                message='Request is data is invalid',
                raw=response)

        if response.status_code == 401:
            
            return ApiResponse(
                response.status_code,
                message='Unauthorized request',
                raw=response)

        if response.status_code in [403, 404]:

            jsonResponse = dict(response.json())

            return ApiResponse(
                response.status_code,
                message=jsonResponse.get('message'),
                raw=response)

        if response.status_code in [200, 201]:

            jsonResponse = dict(response.json())

            data = AddOrUpdateRecordResponse(
                jsonResponse.get('id'),
                jsonResponse.get('warnings'))

            if response.status_code == 200:
                message = 'Record updated successfully'
            else:
                message = 'Record created successfully'

            return ApiResponse(
                response.status_code,
                data,
                message=message,
                raw=response)

        return ApiResponse(
                response.status_code,
                raw=response)

    def DeleteRecordsByIds(self):

        endpoint = DeleteRecordsByIds(self.baseUrl)

        return

    # report methods

    def GetReportById(self, reportId: int):

        endpoint = GetReportByIdEndpoint(self.baseUrl, reportId)

        return

    def GetReportsByAppId(self, appId: int):

        endpoint = GetReportsByAppIdEndpoint(self.baseUrl, appId)

        return