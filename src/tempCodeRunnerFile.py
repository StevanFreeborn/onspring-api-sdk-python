record = Record(195,fields)

response = client.AddOrUpdateRecord(record)

print(f'Status Code: {response.statusCode}')
print(f'Id: {response.data.id}')
for warning in response.data.warnings:
    print(f'Warning: {warning}')