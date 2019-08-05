from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_region_state,
    post_region_state)
import json
from playerstars_interactors import SaveRegionStateException


@patch('playerstars_routes.region_state_route.'
       'GetAllStateRegionsInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_region_state():
    result = get_all_region_state()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_state_route.'
       'GetAllStateRegionsInteractor.run',
       MagicMock(return_value=None))
def teste_get_all_region_state_not_found():
    result = get_all_region_state()

    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "name": "Silver",\
    "minimum_bet" : 1234,\
    "states":["ES", "RJ", "MG"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_state_route.'
       'PostRegionStateInteractor.run')
def test_post_region_country(mock):
    result = post_region_state()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_state_route.'
       'PostRegionStateInteractor.run',
       MagicMock(side_effect=SaveRegionStateException('oops')))
def test_post_region_raises():
    result = post_region_state()

    assert result.body['status'] == 'error'
    assert result.status_code == 500
