from enum import Enum

class DataFormat(Enum):
    """
    The possible data format types for record field values.
    """

    Raw = 0
    Formatted = 1

class ReportDataType(Enum):
    """
    The possible report data types for reports.
    """
    ReportData = 0
    ChartData = 1

class ResultValueType(Enum):
    """
    The possible types for record field values.
    """
    String = 0
    Integer = 1
    Decimal = 2
    Date = 3
    TimeSpan = 4
    Guid = 5
    StringList = 6
    IntegerList = 7
    GuidList = 8
    AttachmentList = 9
    ScoringGroupList = 10
    FileList = 11

class Increment(Enum):
    """
    The possible values for the increment property of timespan data in an Onspring timespan field.
    """
    Seconds = "Second(s)"
    Minutes = "Minute(s)"
    Hours = "Hour(s)"
    Days = "Day(s)"
    Weeks = "Week(s)"
    Months = "Month(s)"
    Years = "Year(s)"

class Recurrence(Enum):
    """
    The possible values for the recurrence property of timespan data in an Onspring timespan field.
    """
    Empty = "None"
    EndByDate = "EndByDate"
    EndAfterOccurrences = 'EndAfterOccurrences'

