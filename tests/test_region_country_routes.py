from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_region_country, RegionCountryRoute,
    post_region_country,
    get_region_country_by_id)
import json
import pytest
from playerstars_interactors import SaveRegionCountryException


@patch('playerstars_routes.region_country_route.'
       'GetAllCountryRegionsInteractor.run')
def test_get_all_region_country(mock):
    result = get_all_region_country()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_country_route.'
       'GetAllCountryRegionsInteractor.run',
       MagicMock(return_value=None))
def test_get_all_region_country_not_found():
    result = get_all_region_country()

    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_country_route.'
       'GetRegionCountryInteractor.run')
def test_get_region_country(mock):
    result = get_region_country_by_id('1d002')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_country_route.'
       'GetRegionCountryInteractor.run',
       MagicMock(return_value=None))
def test_get_region_country_not_found():
    result = get_region_country_by_id('id002')

    assert result.body['message'] == 'Região País não encontrada'
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
    assert result.status_code == 201


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.region_country_route.'
       'PostRegionCountryInteractor.run',
       MagicMock(side_effect=SaveRegionCountryException('oops')))
def test_post_region_raises():
    result = post_region_country()

    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().make_put_request({})
    assert str(exc.value) == 'Update não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().update_exception()
    assert str(exc.value) == 'Update não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().delete_request_model()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().delete_interactor()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().put_interactor()
    assert str(exc.value) == 'Update não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryRoute().delete_not_found()
    assert str(exc.value) == 'Delete não implementado'
