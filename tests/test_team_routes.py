from chalicelib import (
    enter_team,
    get_all_teams,
    get_all_teams_by_user,
    get_team_by_id,
    post_team,
    put_team)
from playerstars_interactors import (
    EnterTeamException,
    SaveTeamException,
    UpdateEntityException,
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


team_image_base_64 = \
    'data:image/svg+xml;utf8;base64,PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxzdmcgeG1' \
    'sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBpZD0iQ2FwYV8xIiBlbmFibGUtY' \
    'mFja2dyb3VuZD0ibmV3IDAgMCA0NDMuMjk0IDQ0My4yOTQiIGhlaWdodD0iMTZweCIgdml' \
    'ld0JveD0iMCAwIDQ0My4yOTQgNDQzLjI5NCIgd2lkdGg9IjE2cHgiPjxwYXRoIGQ9Im0yM' \
    'jEuNjQ3IDBjLTEyMi4yMTQgMC0yMjEuNjQ3IDk5LjQzMy0yMjEuNjQ3IDIyMS42NDdzOTk' \
    'uNDMzIDIyMS42NDcgMjIxLjY0NyAyMjEuNjQ3IDIyMS42NDctOTkuNDMzIDIyMS42NDctM' \
    'jIxLjY0Ny05OS40MzMtMjIxLjY0Ny0yMjEuNjQ3LTIyMS42NDd6bTAgNDE1LjU4OGMtMTA' \
    '2Ljk0MSAwLTE5My45NDEtODctMTkzLjk0MS0xOTMuOTQxczg3LTE5My45NDEgMTkzLjk0M' \
    'S0xOTMuOTQxIDE5My45NDEgODcgMTkzLjk0MSAxOTMuOTQxLTg3IDE5My45NDEtMTkzLjk' \
    '0MSAxOTMuOTQxeiIgZmlsbD0iIzAwMDAwMCIvPjxwYXRoIGQ9Im0yMzUuNSA4My4xMThoL' \
    'TI3LjcwNnYxNDQuMjY1bDg3LjE3NiA4Ny4xNzYgMTkuNTg5LTE5LjU4OS03OS4wNTktNzk' \
    'uMDU5eiIgZmlsbD0iIzAwMDAwMCIvPjwvc3ZnPgo='


def make_post_mock_data():
    payload = {
        'name': 'brazucas',
        'captain': '1235',
        'members': ['pl11'],
        'description': '',
        'image_base64': team_image_base_64
    }
    return MagicMock(
        current_request=MagicMock(json_body=payload,
                                  headers=dict(AUTHORIZATION=jwt)))


def make_put_mock_data():
    payload = {
        'entity_id': 'b1e9c0a7',
        'name': 'DoRio',
        'captain': '123',
        'members': ['pl11'],
        'description': '',
        'consoles': [
            {
                'console_id': '11',
                'name': 'Xbox One',
                'logo_path': '/images/xbox_one.jpg',
                'tag_name': 'nick#1',
                'games': [
                    {
                        'game_id': '01',
                        'name': 'Need for Speed',
                        'logo_path': '/images/nfs.jpg'
                    },
                    {
                        'game_id': '02',
                        'name': 'Fifa 19',
                        'logo_path': '/images/fifa19.jpg'
                    }
                ]
            },
            {
                'console_id': '12',
                'name': 'Nintendo Switch',
                'logo_path': '/images/n_switch.jpg',
                'tag_name': 'nick#2',
                'games': [
                    {
                        'game_id': '01',
                        'name': 'Need for Speed',
                        'logo_path': '/images/nfs.jpg'
                    },
                    {
                        'game_id': '02',
                        'name': 'Fifa 19',
                        'logo_path': '/images/fifa19.jpg'
                    }
                ]
            }
        ],
        'games': [
            {
                'game_id': '01',
                'name': 'Need for Speed',
                'logo_path': '/images/nfs.jpg'
            },
            {
                "game_id": "02",
                "name": "Fifa 19",
                "logo_path": "/images/fifa19.jpg"
            }
        ],
        'image_base64': team_image_base_64
    }
    return MagicMock(
        current_request=MagicMock(json_body=payload,
                                  headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_teams(client, resource, run):
    result = get_all_teams()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_teams_not_found(client, resource):
    result = get_all_teams()
    assert result.body['message'] == 'No team found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team(client, resource, run):
    result = get_team_by_id('team11')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team_not_found(client, resource):
    result = get_team_by_id('team11')
    assert result.body['message'] == 'Team not found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.GetTeamByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team_by_user(client, resource, run):
    result = get_all_teams_by_user('pl11')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.GetTeamByUserInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_teams_by_user_not_found(client, resource):
    result = get_all_teams_by_user('pl11')
    assert result.body['message'] == 'No teams found for this player'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.bp_team', make_post_mock_data())
@patch('chalicelib.team_route.PostTeamInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_team(client, resource, run):
    result = post_team()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.bp_team', make_post_mock_data())
@patch('chalicelib.team_route.PostTeamInteractor.run',
       MagicMock(side_effect=SaveTeamException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_team_raises(client, resource):
    result = post_team()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.bp_team', make_put_mock_data())
@patch('chalicelib.team_route.PutTeamInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_team(client, resource, run):
    result = put_team('id1')
    run.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.bp_team', make_put_mock_data())
@patch('chalicelib.team_route.PutTeamInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_team_raises(client, resource):
    result = put_team('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_enter_team_mock_data():
    payload = """{
    "team_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(json_body=data,
                                  headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.EnterTeamInteractor._recover_team',
       return_value=MagicMock())
@patch('chalicelib.team_route.EnterTeamInteractor._recover_player',
       return_value=MagicMock())
@patch('chalicelib.team_route.bp_team',
       make_enter_team_mock_data())
@patch('chalicelib.team_route.EnterTeamInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_team(client, resource, run, player, duel):
    result = enter_team()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.EnterTeamInteractor._recover_team',
       return_value=MagicMock())
@patch('chalicelib.team_route.EnterTeamInteractor._recover_player',
       return_value=MagicMock())
@patch('chalicelib.team_route.bp_team',
       make_enter_team_mock_data())
@patch('chalicelib.team_route.EnterTeamInteractor.run',
       MagicMock(side_effect=EnterTeamException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_enter_team_raises(client, resource, player, duel):
    result = enter_team()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
