from OnspringClient import OnspringClient
from configparser import ConfigParser
from Models import *

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

request = GetRecordsByAppRequest(195, dataFormat=DataFormat.Formatted.name, fieldIds=[6985,6978])

response = onspringClient.GetRecordsByAppId(request)

print(response.status_code)
print(response.url)
print(response.json())


