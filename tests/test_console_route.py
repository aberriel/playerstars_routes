from chalicelib.console_route import (
    delete_console,
    get_all_console,
    get_all_consoles_admin,
    get_console_by_id,
    get_console_by_id_admin,
    post_console,
    put_console
)
from playerstars_interactors import (
    AccessDeniedAdminException,
    GetConsoleByIdAdminException,
    GetConsolesAdminException,
    SaveEntityException,
    UpdateEntityException
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


def make_get_console_by_id_admin_json_body():
    return {
        'console_id': 'q1w2e3'}


def make_get_console_by_id_admin_mock():
    return MagicMock(current_request=MagicMock(
        json_body=make_get_console_by_id_admin_json_body(),
        headers=dict(AUTHORIZATION=jwt)))


def make_get_consoles_admin_mock():
    return MagicMock(current_request=MagicMock(
        json_body={}, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_consoles_admin_mock())
@patch('chalicelib.console_route.GetConsolesAdminInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin(boto_client, boto_resource, run):
    result = get_all_consoles_admin()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_consoles_admin_mock())
@patch('chalicelib.console_route.GetConsolesAdminInteractor.run',
       MagicMock(return_value=[]))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin_empty(boto_client, boto_resource):
    result = get_all_consoles_admin()
    assert result.body['message'] == 'No console found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_consoles_admin_mock())
@patch('chalicelib.console_route.GetConsolesAdminInteractor.run',
       MagicMock(side_effect=GetConsolesAdminException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin_raises(boto_client, boto_resource):
    result = get_all_consoles_admin()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_consoles_admin_mock())
@patch('chalicelib.console_route.GetConsolesAdminInteractor.run',
       MagicMock(side_effect=AccessDeniedAdminException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin_access_denied(boto_client, boto_resource):
    result = get_all_consoles_admin()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_console_by_id_admin_mock())
@patch('chalicelib.console_route.GetConsoleByIdAdminInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin(boto_client, boto_resource, run):
    result = get_console_by_id_admin()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_console_by_id_admin_mock())
@patch('chalicelib.console_route.GetConsoleByIdAdminInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin_empty(boto_client, boto_resource):
    result = get_console_by_id_admin()
    assert result.body['message'] == 'Console not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_console_by_id_admin_mock())
@patch('chalicelib.console_route.GetConsoleByIdAdminInteractor.run',
       MagicMock(side_effect=GetConsoleByIdAdminException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin_raises(boto_client, boto_resource):
    result = get_console_by_id_admin()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console_admin',
       make_get_console_by_id_admin_mock())
@patch('chalicelib.console_route.GetConsoleByIdAdminInteractor.run',
       MagicMock(side_effect=AccessDeniedAdminException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin_access_denied(boto_client, boto_resource):
    result = get_console_by_id_admin()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles(client, resource, run):
    result = get_all_console()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_not_found(client, resource):
    result = get_all_console()
    assert result.body['message'] == 'No console found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(side_effect=GetConsolesAdminException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_raises(boto_client, boto_resource):
    result = get_all_console()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console(client, resource, run):
    result = get_console_by_id('id1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_not_found(client, resource):
    result = get_console_by_id('id1')
    assert result.body['message'] == 'Console not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_raises(client, resource):
    result = get_console_by_id('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_mock_data():
    payload = """{
    "name": "Super Nintendo",
    "logo_path": "/images/ss.png",
    "tag_name": "nick#1",
    "games" : []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


def make_put_mock_data():
    payload = """{
    "entity_id": "id1",
    "name": "Super Nintendo",
    "logo_path": "/images/ss.png",
    "tag_name": "nick#1",
    "games" : []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console(client, resource, run):
    result = post_console()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_raises(client, resource):
    result = post_console()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console', make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console(client, resource, mock):
    result = put_console('id1')
    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.console_route.bp_console', make_put_mock_data())
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console_raises(client, resource):
    result = put_console('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console(client, resource, mock):
    result = delete_console('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console_not_found(client, resource):
    result = delete_console('id1')
    assert result.body['message'] == 'Console not found to be deleted'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console_raises(client, resource):
    result = delete_console('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
