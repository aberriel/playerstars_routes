import json
from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_consoles, get_console, post_console, put_console, delete_console)
from playerstars_interactors import (
    SaveConsoleException, UpdateConsoleException)


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetAllConsolesInteractor.run')
def test_get_all_games(mock):
    result = get_all_consoles()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetAllConsolesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_consoles()

    assert result.body['message'] == 'Nenhum console encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetConsoleInteractor.run')
def test_get_console(mock):
    result = get_console('id1')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetConsoleInteractor.run',
       MagicMock(return_value=None))
def test_get_console_not_found():
    result = get_console('id1')

    assert result.body['message'] == 'Console não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "name": "Super Nintendo",
    "logo_path": "/images/ss.png",
    "tag_name": "nick#1",
    "games" : []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.console_route.PostConsoleInteractor.run')
def test_post_console(mock):
    result = post_console()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.console_route.PostConsoleInteractor.run',
       MagicMock(side_effect=SaveConsoleException('oops')))
def test_post_console_raises():
    result = post_console()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.PutConsoleInteractor.run')
def test_put_console(mock):
    result = put_console()

    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.PutConsoleInteractor.run',
       MagicMock(side_effect=UpdateConsoleException('oops')))
def test_put_console_raises():
    result = put_console()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.DeleteConsoleInteractor.run')
def test_delete_console(mock):
    result = delete_console('id1')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.DeleteConsoleInteractor.run',
       MagicMock(return_value=None))
def test_delete_console_not_found():
    result = delete_console('id1')

    assert result.body['message'] == 'Console não encontrado para ser deletado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
