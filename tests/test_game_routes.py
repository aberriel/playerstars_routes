import json
from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_games, post_game, GameRoute, get_game_by_id, put_game,
    delete_game)
from playerstars_interactors import SaveGameException, GetAllGamesInteractor, \
    UpdateGameException


@patch('playerstars_routes.game_route.GetAllGamesInteractor.run')
def test_get_all_games(mock):
    result = get_all_games('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetAllGamesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_games('id1')
    assert result.body['message'] == 'Nenhum jogo encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetGameInteractor.run')
def test_get_game_by_id(mock):
    result = get_game_by_id("ID")
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetGameInteractor.run',
       MagicMock(return_value={}))
def test_get_game_not_found():
    result = get_game_by_id("ID")

    assert result.body['message'] == 'Jogo não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "name": "Sonic",
    "logo_path": "images/sonic.jpg",
    "consoles": [{
                "entity_id": "5",
                "name": "Super Nintendo",
                "logo_path": "/images/ss.png",
                "tag_name": "nick#1"
                },{
                "entity_id": "4",
                "name": "Atari",
                "logo_path": "/images/aa.png",
                "tag_name": "nick#2"
                }]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.game_route.PostGameInteractor.run')
def test_post_game(mock):
    result = post_game()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.game_route.PostGameInteractor.run',
       MagicMock(side_effect=SaveGameException('oops')))
def test_post_game_raises():
    result = post_game()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_get_all_interactor():
    assert GameRoute().get_all_interactor() == GetAllGamesInteractor


def make_put_mock_data():
    payload = """{
    "entity_id": "id1",
    "name": "Sonic",
    "logo_path": "images/sonic.jpg",
    "consoles": [{
                "entity_id": "5",
                "name": "Super Nintendo",
                "logo_path": "/images/ss.png",
                "tag_name": "nick#1"
                },{
                "entity_id": "4",
                "name": "Atari",
                "logo_path": "/images/aa.png",
                "tag_name": "nick#2"
                }]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.game_route.PutGameInteractor.run')
def test_put_console(mock):
    result = put_game('id1')

    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.game_route.PutGameInteractor.run',
       MagicMock(side_effect=UpdateGameException('oops')))
def test_put_console_raises():
    result = put_game('id1')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.DeleteGameInteractor.run')
def test_delete_console(mock):
    result = delete_game('id1')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.DeleteGameInteractor.run',
       MagicMock(return_value=None))
def test_delete_console_not_found():
    result = delete_game('id1')

    assert result.body['message'] == 'Game não encontrado para deletar'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
