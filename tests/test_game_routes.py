import json
from unittest.mock import MagicMock, patch
from chalicelib import (
    get_all_games, post_game, get_game_by_id, put_game, delete_game)
from playerstars_interactors import SaveEntityException, UpdateEntityException


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.GetAllGamesInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_games(client, resource, run):
    result = get_all_games('1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.GetAllGamesInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_not_found(client, resource):
    result = get_all_games('1')

    assert result.body['message'] == 'Nenhum jogo encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.GetGameInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console(client, resource, run):
    result = get_game_by_id('id1')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.GetGameInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_not_found(client, resource):
    result = get_game_by_id('id1')

    assert result.body['message'] == 'Game não encontrado'
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
@patch('chalicelib.game_route.bp_game', make_post_mock_data())
@patch('chalicelib.game_route.PostGameInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console(client, resource, run):
    result = post_game()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.bp_game', make_post_mock_data())
@patch('chalicelib.game_route.PostGameInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_raises(client, resource):
    result = post_game()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# def make_put_mock_data():
#     payload = """{
#     "entity_id": "id1",
#     "name": "Sonic",
#     "logo_path": "images/sonic.jpg",
#     "consoles": [{
#                 "entity_id": "5",
#                 "name": "Super Nintendo",
#                 "logo_path": "/images/ss.png",
#                 "tag_name": "nick#1"
#                 },{
#                 "entity_id": "4",
#                 "name": "Atari",
#                 "logo_path": "/images/aa.png",
#                 "tag_name": "nick#2"
#                 }]
#     }"""
#     data = json.loads(payload)
#     return MagicMock(current_request=MagicMock(json_body=data))
#
#
# # noinspection PyUnusedLocal
# @patch('chalicelib.game_route.bp_game', make_put_mock_data())
# @patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
# @patch('boto3.resource')
# @patch('boto3.client')
# def test_put_console(client, resource, mock):
#     result = put_game('id1')
#
#     mock.assert_called_once()
#     assert result.body['data']
#     assert result.body['status'] == 'success'
#     assert result.status_code == 200
#
#
# # noinspection PyUnusedLocal
# @patch('chalicelib.game_route.bp_game', make_put_mock_data())
# @patch('chalicelib.basic_entity_route.BasicPutInteractor.run',
#        MagicMock(side_effect=UpdateEntityException('oops')))
# @patch('boto3.resource')
# @patch('boto3.client')
# def test_put_console_raises(client, resource):
#     result = put_game('id1')
#
#     assert result.body['message'] == 'oops'
#     assert result.body['status'] == 'error'
#     assert result.status_code == 500
#

# noinspection PyUnusedLocal
@patch('chalicelib.game_route.DeleteGameInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console(client, resource, mock):
    result = delete_game('id1')

    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.game_route.DeleteGameInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console_not_found(client, resource):
    result = delete_game('id1')

    assert result.body['message'] == 'Game não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
