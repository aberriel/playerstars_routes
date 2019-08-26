#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from datetime import date, datetime
from playerstars_domain import (
    Console, Game,
    Player, Team, TeamMember,
    User
)
from playerstars_interactors import (
    SaveTeamException,
    UpdateTeamException
)
from playerstars_routes import (
    get_all_teams,
    get_team_by_id,
    get_all_teams_by_user,
    post_team,
    put_team,
    TeamRoute
)
from unittest.mock import MagicMock, patch

import json


def make_post_mock_data():
    payload = """{
        "name": "brazucas",
        "captain": "1235",
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


def make_put_mock_data():
    payload = """{
        "team_id": "b1e9c0a7",
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


def make_game_list():
    game_1 = Game(entity_id='9c3c9101-4e20-4179-8a52-c521a468ae4e',
                  name='Need for Speed',
                  logo_path='/images/nfs.jpg')
    game_2 = Game(entity_id='93b8c9c3-78e9-400f-b67a-8a403c81b1fb',
                  name='Fifa 19',
                  logo_path='/images/fifa19.jog')
    game_3 = Game(entity_id='f80b3866-f38b-47fc-a0f2-f1384f102b1b',
                  name='Fortnite',
                  logo_path='images/fortnite.jpg')
    game_list = [game_1, game_2, game_3]
    return game_list


def make_console_list():
    con_1 = Console(entity_id='aa63650a-0fd4-4e14-8687-6af0d429eca9',
                    name='Xbox One',
                    logo_path='/images/xbox_one.jpg',
                    tag_name='nick#1',
                    games=make_game_list())
    con_2 = Console(entity_id='d1ad5c5a-86a5-4278-af9b-09447fe3fabc',
                    name='Nintendo Switch',
                    logo_path='/images/n_switch.jpg',
                    tag_name='nick#2',
                    games=make_game_list())
    con_3 = Console(entity_id='90a18bd6-f30c-4103-905c-aeb724634808',
                    name='Playstation 4',
                    logo_path='/images/ps4.jpg',
                    tag_name='nick#3',
                    games=make_game_list())
    console_list = [con_1, con_2, con_3]
    return console_list


def make_captain():
    user = User(entity_id='us123',
                name='Anselmo Lira',
                email='anselmo.lira@stormsec.com.br',
                address='Rua dos Alfeneiros, 634',
                city='Hogwarts',
                date_birth=date(1986, 12, 16),
                state='Dartmoor',
                country='England',
                postal_code='634',
                phone_number='5521991996565',
                group='player',
                cpf='123.456.789-01',
                nickname='lira1')
    player = Player(user=user,
                    consoles=make_console_list(),
                    games=make_game_list(),
                    entity_id='1235')
    return player


def make_team_data():
    captain = TeamMember(entity_id='b9e80f49',
                         player=make_captain(),
                         association_date=datetime(2019, 8, 5, 11, 13, 15))
    team = Team(entity_id='b1e9c0a7',
                name='Brazucas',
                captain=captain,
                consoles=make_console_list(),
                games=make_game_list())
    return team


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetAllTeamsInteractor.run')
def test_get_all_teams(mock):
    result = get_all_teams()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetAllTeamsInteractor.run',
       MagicMock(return_value=None))
def test_get_all_teams_not_found():
    result = get_all_teams()
    assert result.body['message'] == 'Nenhum time encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run')
def test_get_team(mock):
    result = get_team_by_id('team11')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run',
       MagicMock(return_value=None))
def test_get_team_not_found():
    result = get_team_by_id('team11')
    assert result.body['message'] == 'Time não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUserInteractor.run')
def test_get_team_by_user(mock):
    result = get_all_teams_by_user('pl11')
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUserInteractor.run',
       MagicMock(return_value=None))
def test_get_teams_by_user_not_found():
    result = get_all_teams_by_user('pl11')
    assert result.body['message'] == 'O jogador não possui times'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.team_route.PostTeamInteractor.run')
def test_post_team(mock):
    result = post_team()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.team_route.PostTeamInteractor.run',
       MagicMock(side_effect=SaveTeamException('oops')))
def test_post_team_raises():
    result = post_team()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.team_route.PutTeamInteractor.run')
@patch('playerstars_routes.team_route.PutTeamInteractor.get_team_from_db',
       return_value=make_team_data())
def test_put_team(saved_team, mock):
    result = put_team('id1')
    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.team_route.PutTeamInteractor.run',
       MagicMock(side_effect=UpdateTeamException('oops')))
@patch('playerstars_routes.team_route.PutTeamInteractor.get_team_from_db',
       return_value=make_team_data())
def test_put_team_raises(saved_team):
    result = put_team('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        TeamRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        TeamRoute().delete_interactor()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        TeamRoute().delete_not_found()
    assert str(exc.value) == 'Não implementado no interactor'
