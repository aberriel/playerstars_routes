import json
from unittest.mock import MagicMock, patch
from chalicelib import \
    get_match_list, post_duel, enter_duel, get_duel, reject_duel_route, \
    get_all_player_duels, get_all_duel, get_duels_by_status_route, end_duel
from playerstars_interactors import (
    EnterDuelException, CreateDuelException, GetPlayerDuelByStatusError,
    RejectDuelException, EndDuelException)
from tests.test_utils import jwt


def make_get_match_list_mock():
    return MagicMock(current_request=MagicMock(
        json_body={}, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_match_list', make_get_match_list_mock())
@patch('chalicelib.duel_route.GetMatchListInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list(client, resource, run):
    result = get_match_list()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_match_list', make_get_match_list_mock())
@patch('chalicelib.duel_route.GetMatchListInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list_not_found(client, resource):
    result = get_match_list()

    assert 'Nenhum match encontrado para o player' in result.body['message']
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "console": {
        "name": "Super Nintendo",
        "logo_path": "/images/ss.png",
        "tag_name": "nick#1",
        "games" : []
        },
    "game":{
        "name": "Sonic",
        "logo_path": "images/sonic.jpg",
        "consoles": []
        },
    "maximum_time": "00:50:00",
    "minimum_time": "00:10:00",
    "bet_size": 90,
    "star_type" : "blue",
    "challenged_id": "idahsiasia"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_create_duel', make_post_mock_data())
@patch('chalicelib.duel_route.CreateDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_create_duel(client, resourcem, run):
    result = post_duel()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_create_duel', make_post_mock_data())
@patch('chalicelib.duel_route.CreateDuelInteractor.run',
       MagicMock(side_effect=CreateDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_create_duel_raises(client, resource):
    result = post_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_enter_duel_mock_data():
    payload = """{
        "duel_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.EnterDuelInteractor._recover_duel',
       return_value=MagicMock())
@patch('chalicelib.duel_route.EnterDuelInteractor._recover_player',
       return_value=MagicMock())
@patch('chalicelib.duel_route.bp_enter_duel',
       make_enter_duel_mock_data())
@patch('chalicelib.duel_route.EnterDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel(client, resource, run, player, duel):
    result = enter_duel()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.EnterDuelInteractor._recover_duel',
       return_value=MagicMock())
@patch('chalicelib.duel_route.EnterDuelInteractor._recover_player',
       return_value=MagicMock())
@patch('chalicelib.duel_route.bp_enter_duel',
       make_enter_duel_mock_data())
@patch('chalicelib.duel_route.EnterDuelInteractor.run',
       MagicMock(side_effect=EnterDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel_raises(client, resource, player, duel):
    result = enter_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_profile_request():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel(client, resource, run):
    result = get_all_player_duels()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel_not_found(client, resource):
    result = get_all_player_duels()

    assert result.body['message'] == \
        'No duel found for the player ' \
        '8ad1635f-2263-4dda-879a-bd24b5d9732f'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_duel(client, resource, run):
    result = get_all_duel()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_duel(client, resource):
    result = get_all_duel()

    assert result.body['message'] == 'No duel found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel(client, resource, run):
    result = get_duel('1234')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_duel(client, resource):
    result = get_duel('123123')

    assert result.body['message'] == 'Duel not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status(client, resource, run):
    result = get_duels_by_status_route('lobby')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status_not_found(client, resource):
    result = get_duels_by_status_route('lobby')

    assert result.body['message'] == \
        "No duel found with status lobby for the player" \
        " 8ad1635f-2263-4dda-879a-bd24b5d9732f"
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_get_profile_request())
@patch('chalicelib.duel_route.GetPlayerDuelByStatusInteractor.run',
       MagicMock(side_effect=GetPlayerDuelByStatusError('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_duel_by_status_not_found_raises(client, resource):
    result = get_duels_by_status_route('lobby')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_reject_request():
    payload = """{
        "duel_id": "id1234"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.duel_route.bp_duel', make_post_reject_request())
@patch('chalicelib.duel_route.RejectDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_reject_duel(client, resource, run):
    result = reject_duel_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_duel', make_post_reject_request())
@patch('chalicelib.duel_route.RejectDuelInteractor.run',
       MagicMock(side_effect=RejectDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def teste_reject_duel_raises(client, resource):
    result = reject_duel_route()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_end_duel_request():
    payload = """{
        "duel_id": "id1234",
        "result": "win",
        "image_base64": "iuasdiuhafiasjdiyhviuasd"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.duel_route.bp_duel', make_end_duel_request())
@patch('chalicelib.duel_route.EndDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_end_duel(client, resource, run):
    result = end_duel()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.duel_route.bp_duel', make_end_duel_request())
@patch('chalicelib.duel_route.EndDuelInteractor.run',
       MagicMock(side_effect=EndDuelException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_end_duel_raises(client, resource):
    result = end_duel()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
