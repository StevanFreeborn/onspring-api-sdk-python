from datetime import datetime
from Enums import *

def parseDate(date: str):

    if date==None:
        return None

    for format in ["%Y-%m-%dT%H:%M:%S.%fZ","%Y-%m-%dT%H:%M:%SZ"]:
            try:
                return datetime.strptime(date, format)
            except ValueError:
                pass

def GetResultValueString(value):
    match value.type:
        case ResultValueType.String.name:
            return value.AsString()

        case ResultValueType.Integer.name:
            return value.AsInteger()

        case ResultValueType.Decimal.name:
            return value.AsDecimal()

        case ResultValueType.Date.name:
            return value.AsDate()

        case ResultValueType.TimeSpan.name:
            data = value.AsTimeSpan()
            return f'Quantity: {data.quantity}, Increment: {data.increment}, Recurrence: {data.recurrence}, EndByDate: {data.endByDate}, EndAfterOccurrences: {data.endAfterOccurrences}'
        
        case ResultValueType.Guid.name:
            return value.AsGuid()
        
        case ResultValueType.StringList.name:
            data = value.AsStringList()
            return f'{",".join(data)}'
        
        case ResultValueType.IntegerList.name:
            data = value.AsIntegerList()
            return f'{",".join([str(i) for i in data])}'
        
        case ResultValueType.GuidList.name:
            data = value.AsGuidList()
            return f'{",".join([str(guid) for guid in data])}'
        
        case ResultValueType.AttachmentList.name:
            data = value.AsAttachmentList()

            strings = []

            for attachment in data:
                string = f'FileId: {attachment.fileId}, FileName: {attachment.fileName}, Notes: {attachment.notes}, StorageLocation: {attachment.storageLocation}'
                strings.append(string)
            
            return f'{"; ".join(strings)}'
        
        case ResultValueType.ScoringGroupList.name:
            data = value.AsScoringGroupList()

            strings = []

            for scoringGroup in data:
                string = f'ListValueId: {scoringGroup.listValueId}, Name: {scoringGroup.name}, Score: {scoringGroup.score}, Max Score: {scoringGroup.maximumScore}'
                strings.append(string)

            return f'{"; ".join(strings)}'
        
        case ResultValueType.FileList.name:
            data = value.AsFileList()
            return f'{",".join([str(i) for i in data])}'