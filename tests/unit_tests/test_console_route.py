from chalicelib.console_route import (
    delete_console,
    get_all_console,
    get_all_consoles_external,
    get_console_by_id,
    post_console,
    put_console,
    get_all_consoles_active_games)
from playerstars_interactors import (
    GetAllConsolesExternalException,
    GetAllConsolesActiveGamesException,
    SaveEntityException,
    UpdateEntityException)
from unittest.mock import MagicMock, patch

import json


prefix_basic_route = 'chalicelib.basic_entity_route'
prefix_console_route = 'chalicelib.console_route'


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicEntityRoute.get_all')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles(client, resource, run):
    get_all_console()
    run.assert_called_once()


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console(client, resource, run):
    result = get_console_by_id('id1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_not_found(client, resource):
    result = get_console_by_id('id1')
    assert result.body['message'] == 'Console not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicGetInteractor.run',
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
@patch(f'{prefix_console_route}.bp_console', make_post_mock_data())
@patch(f'{prefix_basic_route}.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console(client, resource, run):
    result = post_console()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch(f'{prefix_console_route}.bp_console', make_post_mock_data())
@patch(f'{prefix_basic_route}.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_raises(client, resource):
    result = post_console()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch(f'{prefix_console_route}.bp_console', make_put_mock_data())
@patch(f'{prefix_basic_route}.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console(client, resource, mock):
    result = put_console('id1')
    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch(f'{prefix_console_route}.bp_console', make_put_mock_data())
@patch(f'{prefix_basic_route}.BasicPutInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console_raises(client, resource):
    result = put_console('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console(client, resource, mock):
    result = delete_console('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch(f'{prefix_basic_route}.BasicDeleteInteractor.run',
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


@patch(f'{prefix_console_route}.GetAllConsolesExternalInteractor')
@patch(f'{prefix_console_route}.get_console_adapter')
@patch(f'{prefix_console_route}.server_error')
@patch(f'{prefix_console_route}.success')
def test_get_all_consoles_external(mock_success,
                                   mock_server_error,
                                   mock_console_adapter,
                                   mock_interactor):
    consoles = get_all_consoles_external()
    mock_interactor.assert_called_once_with(
        console_adapter=mock_console_adapter())
    mock_interactor().run.assert_called_once()
    mock_success.assert_called_with(mock_interactor().run()())
    mock_server_error.assert_not_called()
    assert consoles == mock_success()


@patch(f'{prefix_console_route}.GetAllConsolesExternalInteractor',
       side_effect=GetAllConsolesExternalException('oops'))
@patch(f'{prefix_console_route}.get_console_adapter')
@patch(f'{prefix_console_route}.server_error')
@patch(f'{prefix_console_route}.success')
def test_get_all_consoles_external_raises(mock_success,
                                          mock_server_error,
                                          mock_console_adapter,
                                          mock_interactor):
    consoles = get_all_consoles_external()
    mock_interactor.assert_called_with(
        console_adapter=mock_console_adapter())
    mock_success.assert_not_called()
    mock_server_error.assert_called_once_with('oops')
    assert consoles == mock_server_error()


@patch(f'{prefix_console_route}.GetAllConsolesActiveGamesInteractor')
@patch(f'{prefix_console_route}.get_console_adapter')
@patch(f'{prefix_console_route}.server_error')
@patch(f'{prefix_console_route}.success')
def test_get_all_consoles_active_games(mock_success,
                                       mock_server_error,
                                       mock_console_adapter,
                                       mock_interactor):
    consoles = get_all_consoles_active_games()
    mock_interactor.assert_called_once_with(
        console_adapter=mock_console_adapter())
    mock_interactor().run.assert_called_once()
    mock_success.assert_called_with(mock_interactor().run()())
    mock_server_error.assert_not_called()
    assert consoles == mock_success()


@patch(f'{prefix_console_route}.GetAllConsolesActiveGamesInteractor',
       side_effect=GetAllConsolesActiveGamesException('oops'))
@patch(f'{prefix_console_route}.get_console_adapter')
@patch(f'{prefix_console_route}.server_error')
@patch(f'{prefix_console_route}.success')
def test_get_all_consoles_active_games_raises(mock_success,
                                              mock_server_error,
                                              mock_console_adapter,
                                              mock_interactor):
    consoles = get_all_consoles_active_games()
    mock_interactor.assert_called_with(
        console_adapter=mock_console_adapter())
    mock_success.assert_not_called()
    mock_server_error.assert_called_once_with('oops')
    assert consoles == mock_server_error()
