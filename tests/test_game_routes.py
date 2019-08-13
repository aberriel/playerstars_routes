import json
import pytest
from unittest.mock import MagicMock, patch
from playerstars_routes import (
    get_all_games, post_game, GameRoute, get_game_by_id)
from playerstars_interactors import SaveGameException


@patch('playerstars_routes.game_route.GetAllGamesInteractor.run')
def test_get_all_games(mock):
    result = get_all_games()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetAllGamesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_games()
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


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().make_put_request()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().update_exception()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().delete_interactor()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().put_interactor()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        GameRoute().delete_not_found()
    assert str(exc.value) == "Não implementado no interactor"
