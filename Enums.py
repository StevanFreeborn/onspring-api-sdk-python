from enum import Enum

class DataFormat(Enum):
    Raw = 0
    Formatted = 1

class ResultValueType(Enum):
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
    Seconds = "Second(s)"
    Minutes = "Minute(s)"
    Hours = "Hour(s)"
    Days = "Day(s)"
    Weeks = "Week(s)"
    Months = "Month(s)"
    Years = "Year(s)"

class Recurrence(Enum):
    Empty = "None"
    EndByDate = "EndByDate"
    EndAfterOccurrences = 'EndAfterOccurrences'

