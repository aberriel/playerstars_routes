from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_region_state,
    get_region_state_by_id, put_region_state,
    post_region_state, RegionStateRoute)
import json
import pytest
from playerstars_interactors import SaveRegionStateException, \
    UpdateRegionStateException


@patch('playerstars_routes.region_state_route.'
       'GetAllRegionStatesInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_region_state():
    result = get_all_region_state()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_state_route.'
       'GetAllRegionStatesInteractor.run',
       MagicMock(return_value=None))
def teste_get_all_region_state_not_found():
    result = get_all_region_state()

    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_state_route.GetRegionStateInteractor.run')
def test_get_region_state(mock):
    result = get_region_state_by_id('1d001')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_state_route.GetRegionStateInteractor.run',
       MagicMock(return_value=None))
def test_get_region_state_not_found():
    result = get_region_state_by_id('id001')

    assert result.body['message'] == 'Região Estado não encontrada'
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
    assert result.status_code == 201


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_state_route.'
       'PostRegionStateInteractor.run',
       MagicMock(side_effect=SaveRegionStateException('oops')))
def test_post_region_raises():
    result = post_region_state()

    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_put_mock_data():
    payload = """{
    "entity_id": "id123",
    "name": "Gold",\
    "minimum_bet" : 1234,\
    "states":["RJ", "RS", "ES"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.region_state_route.'
       'PutRegionStateInteractor.run')
def test_put_region_country(mock):
    result = put_region_state("id123")

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.region_state_route.'
       'PutRegionStateInteractor.run',
       MagicMock(side_effect=UpdateRegionStateException('oops')))
def test_put_region_raises():
    result = put_region_state("14")

    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        RegionStateRoute().delete_request_model()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionStateRoute().delete_interactor()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionStateRoute().delete_not_found()
    assert str(exc.value) == 'Delete não implementado'
