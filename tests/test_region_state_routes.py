from unittest.mock import MagicMock, patch
from chalicelib import (
    get_all_region_state,
    get_region_state_by_id,
    put_region_state,
    post_region_state)
import json
from playerstars_interactors import SaveEntityException, UpdateEntityException


@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_region_state(client, resource, run):
    result = get_all_region_state()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_region_state_not_found(clien, resource):
    result = get_all_region_state()

    assert result.body['message'] == 'No region-state found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_region_state(client, resource, run):
    result = get_region_state_by_id('1d001')

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_region_state_not_found(client, resource):
    result = get_region_state_by_id('id001')

    assert result.body['message'] == 'Region-state not found'
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
@patch('chalicelib.region_state_route.bp_region_state',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_region_country(client, resource, run):
    result = post_region_state()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


@patch('chalicelib.region_state_route.bp_region_state',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_region_raises(client, resource):
    result = post_region_state()

    assert result.body['message'] == 'oops'
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
@patch('chalicelib.region_state_route.bp_region_state',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_region_country(client, resource, run):
    result = put_region_state("id123")

    run.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.region_state_route.bp_region_state',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_region_raises(client, resource):
    result = put_region_state("14")

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
