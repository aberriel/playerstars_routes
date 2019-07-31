import json
from unittest.mock import MagicMock, patch
from playerstars_routes import get_all_games, post_game
from playerstars_interactors import SaveGameException

@patch('playerstars_routes.game_route.GetAllGamesInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_games():
    result = get_all_games()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetAllGamesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_games()

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
def test_post_user(mock):
    result = post_game()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.game_route.PostGameInteractor.run',
       MagicMock(side_effect=SaveGameException('oops')))
def test_post_user_raises():
    result = post_game()

    assert result.body['status'] == 'error'
    assert result.status_code == 500
