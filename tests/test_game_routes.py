from unittest.mock import MagicMock, patch
from playerstars_routes import get_all_games


@patch('playerstars_routes.game_route.GetAllConsolesInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_games():
    result = get_all_games()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.game_route.GetAllConsolesInteractor.run',
       MagicMock(return_value=None))
def test_get_all_games_not_found():
    result = get_all_games()

    assert result.body['status'] == 'error'
    assert result.status_code == 404
