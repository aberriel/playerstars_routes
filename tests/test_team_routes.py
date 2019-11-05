from unittest.mock import MagicMock, patch
import json
from playerstars_interactors import (
    SaveEntityException, UpdateEntityException, EnterTeamException
)

from chalicelib import (
    get_all_teams, get_team_by_id, get_all_teams_by_user, post_team,
    put_team, enter_team)


def make_post_mock_data():
    payload = """{
        "name": "brazucas",
        "captain": "1235",
        "members": ["pl11"],
        "consoles": [],
        "games": [],
        "description": ""
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


def make_put_mock_data():
    payload = """{
        "entity_id": "b1e9c0a7",
        "name": "DoRio",
        "captain": "123",
        "members": ["pl11"],
        "consoles": [
            {
                "console_id": "11",
                "name": "Xbox One",
                "logo_path": "/images/xbox_one.jpg",
                "tag_name": "nick#1",
                "games": [
                    {
                        "game_id": "01",
                        "name": "Need for Speed",
                        "logo_path": "/images/nfs.jpg"
                    },
                    {
                        "game_id": "02",
                        "name": "Fifa 19",
                        "logo_path": "/images/fifa19.jpg"
                    }
                ]
            },
            {
                "console_id": "12",
                "name": "Nintendo Switch",
                "logo_path": "/images/n_switch.jpg",
                "tag_name": "nick#2",
                "games": [
                    {
                        "game_id": "01",
                        "name": "Need for Speed",
                        "logo_path": "/images/nfs.jpg"
                    },
                    {
                        "game_id": "02",
                        "name": "Fifa 19",
                        "logo_path": "/images/fifa19.jpg"
                    }
                ]
            }
        ],
        "games": [
            {
                "game_id": "01",
                "name": "Need for Speed",
                "logo_path": "/images/nfs.jpg"
            },
            {
                "game_id": "02",
                "name": "Fifa 19",
                "logo_path": "/images/fifa19.jpg"
            }
        ]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


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
    assert result.body['message'] == 'Nenhum team encontrado'
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
    assert result.body['message'] == 'Team não encontrado'
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
    assert result.body['message'] == 'Não foram ' \
                                     'encontradas teams para esse player'
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
       MagicMock(side_effect=SaveEntityException('oops')))
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
    "player_id": "userid#123",
    "team_id": "duelid123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.team_route.EnterTeamInteractor._recover_team',
       return_value=MagicMock())
@patch('chalicelib.team_route.EnterTeamInteractor._recover_player',
       return_value=MagicMock())
@patch('chalicelib.team_route.bp_enter_team',
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
@patch('chalicelib.team_route.bp_enter_team',
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
