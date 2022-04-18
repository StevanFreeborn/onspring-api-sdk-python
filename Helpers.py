from datetime import datetime

def parseDate(date: str):

    if date==None:
        return None

    for format in ["%Y-%m-%dT%H:%M:%S.%fZ","%Y-%m-%dT%H:%M:%SZ"]:
            try:
                return datetime.strptime(date, format)
            except ValueError:
                pass