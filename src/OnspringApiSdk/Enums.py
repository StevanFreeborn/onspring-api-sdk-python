from enum import Enum

class DataFormat(Enum):
    """
    The possible data format types for record field values.
    """

    Raw:int = 0
    Formatted:int = 1

class ReportDataType(Enum):
    """
    The possible report data types for reports.
    """
    ReportData:int = 0
    ChartData:int = 1

class ResultValueType(Enum):
    """
    The possible types for record field values.
    """
    String:int = 0
    Integer:int = 1
    Decimal:int = 2
    Date:int = 3
    TimeSpan:int = 4
    Guid:int = 5
    StringList:int = 6
    IntegerList:int = 7
    GuidList:int = 8
    AttachmentList:int = 9
    ScoringGroupList:int = 10
    FileList:int = 11

class Increment(Enum):
    """
    The possible values for the increment property of timespan data in an Onspring timespan field.
    """
    Seconds:str = "Second(s)"
    Minutes:str = "Minute(s)"
    Hours:str = "Hour(s)"
    Days:str = "Day(s)"
    Weeks:str = "Week(s)"
    Months:str = "Month(s)"
    Years:str = "Year(s)"

class Recurrence(Enum):
    """
    The possible values for the recurrence property of timespan data in an Onspring timespan field.
    """
    Empty:str = "None"
    EndByDate:str = "EndByDate"
    EndAfterOccurrences:str = 'EndAfterOccurrences'

