from unittest.mock import MagicMock, patch
from playerstars_routes.match_list_route import get_match_list


# noinspection PyUnusedLocal
@patch('playerstars_routes.match_list_route.GetMatchListInteractor.run')
def test_get_console(mock):
    # result = ConsoleRoute().get_console('id1')
    result = get_match_list('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.match_list_route.GetMatchListInteractor.run',
       MagicMock(return_value=None))
def test_get_console_not_found():
    result = get_match_list('id1')

    assert result.body['message'] == 'Nenhum match encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
