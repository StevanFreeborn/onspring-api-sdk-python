import sys

import requests_mock

sys.path.append('src')

from OnspringApiSdk.OnspringClient import OnspringClient


@requests_mock.Mocker(kw='mock')
class TestOnspringClient(object):
    test_url = 'https://test.com'
    test_apiKey = 'apiKey'
    client = OnspringClient(test_url, test_apiKey)

    def test_GetFieldsByAppId_WhenFieldContainsListValues_ItShouldReturnThoseValues(self, **kwargs):
        mockResponse = {
            "pageNumber": 1,
            "pageSize": 2,
            "totalPages": 1,
            "totalRecords": 2,
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
                },
            ]
        }

        kwargs['mock'].get(self.test_url + '/Fields/appId/1', json=mockResponse)
        
        response = self.client.GetFieldsByAppId(1)
        
        field_4801 = response.data.fields[0]
        field_4815 = response.data.fields[1]
        
        assert field_4801.id == 4801, "Field id should be 4801"
        assert field_4801.listId == 638, "Field list id should be 638"
        assert field_4801.multiplicity == "SingleSelect", "Field multiplicity should be SingleSelect"
        assert field_4801.values is not None, "Field list values should not be None"

        field_4801_value = field_4801.values[0]

        assert field_4801_value.id == "2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84", "Field value id should be 2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84"
        assert field_4801_value.name == "list_value_1", "Field value name should be list_value_1"
        assert field_4801_value.sortOrder == 1, "Field value sort order should be 1"
        assert field_4801_value.numericValue == 1, "Field value numeric value should be 1"
        assert field_4801_value.color == "#008e8e", "Field value color should be #008e8e"

        assert field_4815.id == 4815, "Field id should be 4815"
        assert field_4815.listId is None, "Field list id should be None"
        assert field_4815.multiplicity is None, "Field multiplicity should be None"
        assert field_4815.values is not None, "Field list values should not be None"
        assert field_4815.outputType == 'ListValue', 'Field output type should be ListValue'

        field_4815_value = field_4815.values[0]

        assert field_4815_value.id == "b235afb2-b786-4c87-bce9-fbd700e246c1", "Field value id should be b235afb2-b786-4c87-bce9-fbd700e246c1"
        assert field_4815_value.name == "list_value_1", "Field value name should be list_value_1"
        assert field_4815_value.sortOrder == 1, "Field value sort order should be 1"
        assert field_4815_value.numericValue == 1, "Field value numeric value should be 1"
        assert field_4815_value.color == "#6dcff6", "Field value color should be #6dcff6"

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
        
        field_4801 = response.data.fields[0]
        field_4815 = response.data.fields[1]
        
        assert field_4801.id == 4801, "Field id should be 4801"
        assert field_4801.listId == 638, "Field list id should be 638"
        assert field_4801.multiplicity == "SingleSelect", "Field multiplicity should be SingleSelect"
        assert field_4801.values is not None, "Field list values should not be None"

        field_4801_value = field_4801.values[0]

        assert field_4801_value.id == "2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84", "Field value id should be 2c1af5b1-0f90-4378-b9a5-8b7e22f2bc84"
        assert field_4801_value.name == "list_value_1", "Field value name should be list_value_1"
        assert field_4801_value.sortOrder == 1, "Field value sort order should be 1"
        assert field_4801_value.numericValue == 1, "Field value numeric value should be 1"
        assert field_4801_value.color == "#008e8e", "Field value color should be #008e8e"

        assert field_4815.id == 4815, "Field id should be 4815"
        assert field_4815.listId is None, "Field list id should be None"
        assert field_4815.multiplicity is None, "Field multiplicity should be None"
        assert field_4815.values is not None, "Field list values should not be None"
        assert field_4815.outputType == 'ListValue', 'Field output type should be ListValue'

        field_4815_value = field_4815.values[0]

        assert field_4815_value.id == "b235afb2-b786-4c87-bce9-fbd700e246c1", "Field value id should be b235afb2-b786-4c87-bce9-fbd700e246c1"
        assert field_4815_value.name == "list_value_1", "Field value name should be list_value_1"
        assert field_4815_value.sortOrder == 1, "Field value sort order should be 1"
        assert field_4815_value.numericValue == 1, "Field value numeric value should be 1"
        assert field_4815_value.color == "#6dcff6", "Field value color should be #6dcff6"