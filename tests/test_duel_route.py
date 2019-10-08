import json
from unittest.mock import MagicMock, patch
from chalicelib import get_match_list, post_duel, enter_duel
from playerstars_interactors import SaveEntityException, CreateDuelException


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
    "player_id": "userid#123"
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
@patch('chalicelib.duel_route.bp_enter_duel',
       make_enter_duel_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel(client, resource, run):
    result = enter_duel()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.duel_route.bp_enter_duel', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_duel_raises(client, resource):
    result = enter_duel()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
