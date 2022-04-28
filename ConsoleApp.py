import sys

from OnspringClient import OnspringClient
from configparser import ConfigParser

from Models import *
from Enums import *
from Commands import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspring = OnspringClient(url, key)

def main():

    argsLength = len(sys.argv)

    if not argsLength > 1:
        print('No valid command given')
        return

    command = sys.argv[1].lower()

    if command =='connect':
        PrintCanConnect(onspring)
        
    if command == 'getapps':
        PrintGetApps(onspring)
    
    if command == 'getappbyid':
        PrintGetAppById(onspring, 195)
        
    if command == 'getappsbyids':
        PrintGetAppsByIds(onspring, [195, 240])

    if command == 'getfieldbyid':
        PrintGetFieldById(onspring, 9686 )
        return
    
    if command == 'getfileinfobyid':

        if not argsLength > 4:
            print('Please provide record id, fieldId, and fileId values')
            return

        recordId = sys.argv[2]
        fieldId = sys.argv[3]
        fileId = sys.argv[4]

        PrintGetFileInfoById(onspring, recordId, fieldId, fileId)
        return

        PrintGetFileById(onspring, )
        return

    if command == 'savefile':
        PrintSaveFile(
            onspring,
            'C:\\Users\\sfree\\OneDrive\\Desktop\\Test Attachment.txt',
            60,
            6989
        )
    
    if command == 'getrecordsbyappid':
        PrintGetRecordsByAppId(onspring, 195)
        return
    
    if command == 'getrecordbyid':
        PrintGetRecordById(onspring, 195, 3,dataFormat=DataFormat.Raw.name)
        return
    
    if command == 'deleterecord':
        PrintDeleteRecord(onspring, 195, sys.argv[2])
        return
    
    if command == 'getrecordsbyids':
        PrintGetRecordsByIds(onspring, 195, [1, 2], [6983, 6984])
        return

    if command == 'queryrecords':
        fieldId = 6983
        operator = 'eq'
        value = '\'Test Task 5\''
        PrintQueryRecords(onspring, 195, f'{fieldId} {operator} {value}')
        return

    if command == 'addrecord':
        
        fields = [
            StringFieldValue(6983, 'A New Test Task'),
            StringFieldValue(6984, 'This is a test task.')
        ]

        PrintAddOrUpdateRecord(onspring, 195, fields)
        return

    if command == 'updaterecord':

        fields = [
            StringFieldValue(6983, 'Updated'),
            StringFieldValue(6984, 'Updated')
        ]

        PrintAddOrUpdateRecord(onspring, 195, fields, 60)
        return
    
    if command == 'deleterecordsbyids':

        appId = sys.argv[2]

        ids = sys.argv[3].split(',')

        recordIds = [int(id) for id in ids]

        PrintDeleteRecordsByIds(onspring, appId, recordIds)
        return

    if command == 'getreportbyid':

        if not argsLength > 2:
            print('Please provide report id value')
            return

        reportId = sys.argv[2]
        
        if argsLength > 3:
            apiDataFormat = sys.argv[3]
        else:
            apiDataFormat = DataFormat.Raw.name

        if argsLength > 4:
            dataType = sys.argv[4]
        else:
            dataType = ReportDataType.ReportData.name

        PrintGetReportById(onspring, reportId, apiDataFormat, dataType)
        return

    if command == 'getreportsbyappid':

        if not argsLength > 2:
            print('Please provide app id value')
            return

        appId = sys.argv[2]

        PrintGetReportsByAppId(onspring, appId)
        return
    
    print('No valid command given')
    return

if __name__ == "__main__":
    main()