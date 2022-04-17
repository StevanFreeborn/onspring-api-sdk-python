from OnspringClient import OnspringClient
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

key = cfg['prod']['key']
url = cfg['prod']['url']

onspringClient = OnspringClient(url, key)

response =onspringClient.GetAppById(8)

print(response.statusCode)
print(response.isSuccessful)
print(response.message)
print(response.responseText)
print(response.headers)
print(response.data.app.href)
print(response.data.app.id)
print(response.data.app.name)

