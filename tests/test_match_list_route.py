import json
from unittest.mock import MagicMock, patch
from playerstars_routes.match_list_route import get_match_list, post_match
from playerstars_interactors import SendMatchException


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


def make_post_mock_data():
    payload = """{
    "user_id": "userid#123",
    "challenged_id": "userid#4532"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.match_list.SendMatchInterator.run')
def test_post_console(mock):
    result = post_match()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.match_list.SendMatchInterator.run',
       MagicMock(side_effect=SendMatchException('oops')))
def test_post_console_raises():
    result = post_match()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
