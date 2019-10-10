import json
from unittest.mock import MagicMock, patch
from chalicelib import \
    get_match_list, post_duel, enter_duel, \
    get_all_player_duels, get_all_duel
from playerstars_interactors import EnterDuelException, CreateDuelException


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list(client, resource, run):
    result = get_match_list('id1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_match_list_not_found(client, resource):
    result = get_match_list('id1')

    assert result.body['message'] == 'Player não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "player_id": "userid#123",
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
    "star_type" : "blue"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


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
    "player_id": "userid#123",
    "duel_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


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


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel(client, resource, run):
    result = get_all_player_duels('1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.GetAllPlayerDuelInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_duel_not_found(client, resource):
    result = get_all_player_duels('1')

    assert result.body['message'] == \
        'Nenhum duel não encontrado para o player'
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

    assert result.body['message'] == 'Nenhum duel encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
