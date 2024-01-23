import sys

import requests_mock

sys.path.append('src')

from OnspringApiSdk.OnspringClient import OnspringClient


@requests_mock.Mocker(kw='mock')
class TestOnspringClient(object):
    test_url = 'https://test.com'
    test_apiKey = 'apiKey'
    client = OnspringClient(test_url, test_apiKey)

    def test_GetFieldsByIds_WhenFieldContainsListValues_ItShouldReturnThoseValues(self, **kwargs):
        mockResponse = {
            "count": 2,
            "items": [
                {
                "multiplicity": "SingleSelect",
                "listId": 638,
                "values": [
                    {
                    "id": "2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84",
                    "name": "list_value_1",
                    "sortOrder": 1,
                    "numericValue": 1,
                    "color": "#008e8e"
                    },
                    {
                    "id": "0421e502-7f76-480a-9311-363aca3560bc",
                    "name": "list_value_2",
                    "sortOrder": 2,
                    "numericValue": 2,
                    "color": "#a186be"
                    },
                    {
                    "id": "285b91c1-5800-47cb-a030-8cf7cdd7cdf1",
                    "name": "updated_list_value_1676840661138}",
                    "sortOrder": 3,
                    "numericValue": 1,
                    "color": "#000000"
                    }
                ],
                "id": 4801,
                "appId": 130,
                "name": "single_select_list_field",
                "type": "List",
                "status": "Enabled",
                "isRequired": True,
                "isUnique": False
                },
                {
                "outputType": "ListValue",
                "values": [
                    {
                    "id": "b235afb2-b786-4c87-bce9-fbd700e246c1",
                    "name": "list_value_1",
                    "sortOrder": 1,
                    "numericValue": 1,
                    "color": "#6dcff6"
                    },
                    {
                    "id": "5cd7cd55-d6a6-40e0-a560-8aa407c13210",
                    "name": "list_value_2",
                    "sortOrder": 2,
                    "numericValue": 2,
                    "color": "#8e468e"
                    }
                ],
                "id": 4815,
                "appId": 130,
                "name": "list_formula_field",
                "type": "Formula",
                "status": "Enabled",
                "isRequired": False,
                "isUnique": False
                }
            ]
        }

        kwargs['mock'].post(self.test_url + '/Fields/batch-get', json=mockResponse)
        
        response = self.client.GetFieldsByIds([4801, 4815])
        
        assert response.data.fields[0].id == 4801, "Field id should be 4801"
        assert response.data.fields[1].id == 4815, "Field id should be 4815"

        for field in response.data.fields:
            assert field.values is not None, "Field list values should not be None"