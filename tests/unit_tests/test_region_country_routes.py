from unittest.mock import MagicMock, patch
from chalicelib import (
    get_all_region_country,
    get_region_country_by_id,
    put_region_country,
    post_region_country)
import json
from playerstars_interactors import SaveEntityException, UpdateEntityException


@patch('chalicelib.basic_entity_route.BasicEntityRoute.get_all')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_region_country(client, resource, run):
    get_all_region_country()
    run.assert_called_once()


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_region_country(client, resource, run):
    result = get_region_country_by_id('1d001')

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_region_country_not_found(client, resource):
    result = get_region_country_by_id('id001')

    assert result.body['message'] == 'Region-country not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "name": "Silver",\
    "minimum_bet" : 1234,\
    "countries":["ES", "RJ", "MG"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.region_country_route.bp_region_country',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_region_country(client, resource, run):
    result = post_region_country()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


@patch('chalicelib.region_country_route.bp_region_country',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_region_raises(client, resource):
    result = post_region_country()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_put_mock_data():
    payload = """{
    "entity_id": "id123",
    "name": "Gold",\
    "minimum_bet" : 1234,\
    "countries":["RJ", "RS", "ES"]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.region_country_route.bp_region_country',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_region_country(client, resource, run):
    result = put_region_country("id123")

    run.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.region_country_route.bp_region_country',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_region_raises(client, resource):
    result = put_region_country("14")

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
