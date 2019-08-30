import json
import pytest
from unittest.mock import MagicMock, patch
from playerstars_routes import get_match_list, post_duel, \
    MatchListChaliceRoute, enter_duel
from playerstars_interactors import CreateDuelException, EnterDuelException


# noinspection PyUnusedLocal
@patch('playerstars_routes.duel_route.GetMatchListInteractor.run')
def test_get_match_list(mock):
    # result = ConsoleChaliceRoute().get_console('id1')
    result = get_match_list('id1')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.duel_route.GetMatchListInteractor.run',
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
@patch('playerstars_routes.duel_route.CreateDuelInteractor.run')
def test_create_duel(mock):
    result = post_duel()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.duel_route.CreateDuelInteractor.run',
       MagicMock(side_effect=CreateDuelException('oops')))
def test_create_duel_raises():
    result = post_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_enter_duel_mock_data():
    payload = """{
    "player_id": "userid#123",
    "duel_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


@patch('app.app', make_enter_duel_mock_data())
@patch('playerstars_routes.duel_route.EnterDuelInteractor.run')
def test_enter_duel(mock):
    result = enter_duel()

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_enter_duel_mock_data())
@patch('playerstars_routes.duel_route.EnterDuelInteractor.run',
       MagicMock(side_effect=EnterDuelException('oops')))
def test_enter_duel_raises():
    result = enter_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().delete_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().delete_not_found()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().make_put_request({})
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().get_all_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().put_interactor()
    assert str(exc.value) == 'Não implementado'
    with pytest.raises(NotImplementedError) as exc:
        MatchListChaliceRoute().update_exception()
    assert str(exc.value) == 'Não implementado'
    assert MatchListChaliceRoute().not_found_all_message() == \
        'Não implementado'
