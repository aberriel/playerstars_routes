import json
import pytest
from unittest.mock import MagicMock, patch
from playerstars_routes import get_match_list, post_duel, \
    MatchListRoute
from playerstars_interactors import CreateDuelException


# noinspection PyUnusedLocal
@patch('playerstars_routes.match_route.GetMatchListInteractor.run')
def test_get_match_list(mock):
    # result = ConsoleRoute().get_console('id1')
    result = get_match_list('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.match_route.GetMatchListInteractor.run',
       MagicMock(return_value=None))
def test_get_match_list_not_found():
    result = get_match_list('id1')

    assert result.body['message'] == 'Nenhum match encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "player_id": "userid#123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.match_route.CreateDuelInteractor.run')
def test_create_duel(mock):
    result = post_duel()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.match_route.CreateDuelInteractor.run',
       MagicMock(side_effect=CreateDuelException('oops')))
def test_create_duel_raises():
    result = post_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().delete_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().delete_not_found()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().make_put_request({})
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().get_all_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().put_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListRoute().update_exception()
    assert str(exc.value) == 'Não implementado'
    assert MatchListRoute().not_found_all_message() == 'Não implementado'
