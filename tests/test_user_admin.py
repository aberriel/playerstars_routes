from unittest.mock import MagicMock, patch
from chalicelib import (
    post_user_admin, get_user_admin_by_id, get_all_user_admin, put_user_admin)
from playerstars_interactors import SaveEntityException, UpdateEntityException

import json


def make_post_mock_data():
    payload = """{
        "name": "Anselmo Lira",
        "email": "playerstars@playerstars.com.br"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.user_admin_route.bp_user_admin',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_user_admin(client, resource, run):
    result = post_user_admin()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.user_admin_route.bp_user_admin',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_user_admin_raises(client, resource):
    result = post_user_admin()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_user_admin(client, resource, run):
    result = get_user_admin_by_id('1d001')

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_user_admin_not_found(client, resource):
    result = get_user_admin_by_id('id001')

    assert result.body['message'] == 'User-admin not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_user_admin(client, resource, run):
    result = get_all_user_admin()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_user_admin_not_found(client, resource):
    result = get_all_user_admin()

    assert result.body['message'] == 'No user-admin found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_put_mock_data():
    payload = """{
        "name": "Anselmo Lira",
        "email": "playerstars@playerstars.com.br",
        "entity_id": "1212354"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.user_admin_route.bp_user_admin',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_user_admin(client, resource, run):
    result = put_user_admin("id123")

    run.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.user_admin_route.bp_user_admin',
       make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_region_raises(client, resource):
    result = put_user_admin("14")

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
