from unittest.mock import MagicMock, patch
from playerstars_routes import get_all_region_country, post_region_country
import json
from playerstars_interactors import SaveRegionCountryException


@patch('playerstars_routes.region_country_route.'
       'GetAllCountryRegionsInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_region_country():
    result = get_all_region_country()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_country_route.'
       'GetAllCountryRegionsInteractor.run',
       MagicMock(return_value=None))
def teste_get_all_region_country_not_found():
    result = get_all_region_country()

    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "name": "Gold",\
    "minimum_bet" : 1234,\
    "countries":["Brasil", "Venezuela", "Cuba"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_country_route.'
       'PostRegionCountryInteractor.run')
def test_post_region_country(mock):
    result = post_region_country()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_country_route.'
       'PostRegionCountryInteractor.run',
       MagicMock(side_effect=SaveRegionCountryException('oops')))
def test_post_region_raises():
    result = post_region_country()

    assert result.body['status'] == 'error'
    assert result.status_code == 500
