from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_region_country, RegionCountryChaliceRoute,
    post_region_country, put_region_country,
    get_region_country_by_id)
import json
import pytest
from playerstars_interactors import SaveRegionCountryException, \
    UpdateRegionCountryException


@patch('playerstars_routes.region_country_route.'
       'GetAllRegionCountriesInteractor.run')
def test_get_all_region_country(mock):
    result = get_all_region_country()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_country_route.'
       'GetAllRegionCountriesInteractor.run',
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

    mock.assert_called_once()
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


def make_put_mock_data():
    payload = """{
    "entity_id": "id123",
    "name": "Gold",\
    "minimum_bet" : 1234,\
    "countries":["Brasil", "Venezuela", "Cuba"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.region_country_route.'
       'PutRegionCountryInteractor.run')
def test_put_region_country(mock):
    result = put_region_country("id123")

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.region_country_route.'
       'PutRegionCountryInteractor.run',
       MagicMock(side_effect=UpdateRegionCountryException('oops')))
def test_put_region_raises():
    result = put_region_country("010101")

    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryChaliceRoute().delete_request_model()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryChaliceRoute().delete_interactor()
    assert str(exc.value) == 'Delete não implementado'
    with pytest.raises(NotImplementedError) as exc:
        RegionCountryChaliceRoute().delete_not_found()
    assert str(exc.value) == 'Delete não implementado'
