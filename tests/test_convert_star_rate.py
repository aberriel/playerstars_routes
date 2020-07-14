from chalicelib.convert_star_rate_route import (
    delete_convert_rate,
    get_all_convert_rate,
    get_convert_rate_by_id,
    post_convert_rate,
    put_convert_rate
)
from playerstars_interactors import SaveEntityException, UpdateEntityException
from unittest.mock import MagicMock, patch

import json


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_convert_rate(client, resource, run):
    result = get_all_convert_rate()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_convert_rate_not_found(client, resource):
    result = get_all_convert_rate()

    assert result.body['message'] == 'No convert-rate found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_convert_rate_raises(client, resource):
    result = get_all_convert_rate()

    assert 'oops' in result.body['message']
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_convert_rate(client, resource, run):
    result = get_convert_rate_by_id('id1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_convert_rate_not_found(client, resource):
    result = get_convert_rate_by_id('id1')

    assert result.body['message'] == 'Convert-rate not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_convert_rate_raises(client, resource):
    result = get_convert_rate_by_id('id1')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_mock_data():
    payload = """{
    "convert_rate": 4
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


def make_put_mock_data():
    payload = """{
    "entity_id": "id1",
    "conver_rate": 5
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.convert_star_rate_route.bp_convert', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_convert_rate(client, resource, run):
    result = post_convert_rate()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.convert_star_rate_route.bp_convert', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_convert_rate_raises(client, resource):
    result = post_convert_rate()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.convert_star_rate_route.bp_convert', make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_convert_rate(client, resource, mock):
    result = put_convert_rate('id1')

    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.convert_star_rate_route.bp_convert', make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_convert_rate_raises(client, resource):
    result = put_convert_rate('id1')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_convert_rate(client, resource, mock):
    result = delete_convert_rate('id1')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_convert_rate_not_found(client, resource):
    result = delete_convert_rate('id1')

    assert result.body['message'] == 'Convert-rate not found to be deleted'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_convert_rate_raises(client, resource):
    result = delete_convert_rate('id1')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
