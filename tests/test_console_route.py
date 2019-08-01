import json
from unittest.mock import MagicMock, patch
from playerstars_routes import get_all_consoles, get_console, post_console
from playerstars_interactors import SaveConsoleException


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetAllConsolesInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_games():
    result = get_all_consoles()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetAllConsolesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_consoles()

    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetConsoleInteractor.run',
       MagicMock(return_value='ok'))
def test_get_console():
    result = get_console('id1')

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.console_route.GetConsoleInteractor.run',
       MagicMock(return_value=None))
def test_get_console_not_found():
    result = get_console('id1')

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
def test_post_user(mock):
    result = post_console()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.console_route.PostConsoleInteractor.run',
       MagicMock(side_effect=SaveConsoleException('oops')))
def test_post_user_raises():
    result = post_console()

    assert result.body['status'] == 'error'
    assert result.status_code == 500
