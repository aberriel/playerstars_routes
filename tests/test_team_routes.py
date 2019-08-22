#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_interactors import(
    SaveTeamException,
    UpdateTeamException
)
from playerstars_routes import (
    get_all_teams,
    get_team_by_id,
    get_all_teams_by_user,
    post_team,
    put_team
)
from unittest.mock import MagicMock, patch

import pytest


def make_game_data():
    data = [
        {
            "entity_id": "01",
            "name": "Need for Speed",
            "logo_path": "/images/nfs.jpg"
        },
        {
            "entity_id": "02",
            "name": "Fifa 19",
            "logo_path": "/images/fifa19.jpg"
        },
        {
            "entity_id": "03",
            "name": "Fortnite",
            "logo_path": "/images/fortnite.jpg"
        },
        {
            "entity_id": "04",
            "name": "CS Go",
            "logo_path": "/images/csgo.jpg"
        }
    ]
    return data


def make_console_data():
    data = [
        {
            "entity_id": "11",
            "name": "Xbox One",
            "logo_path": "/images/xbox_one.jpg",
            "tag_name": "nick#1",
            "games": make_game_data()
        },
        {
            "entity_id": "12",
            "name": "Nintendo Switch",
            "logo_path": "/images/n_switch.jpg",
            "tag_name": "nick#2",
            "games": make_game_data()
        },
        {
            "entity_id": "13",
            "name": "Playstation 4",
            "logo_path": "/images/ps4.jpg",
            "tag_name": "nick#3",
            "games": make_game_data()
        },
        {
            "entity_id": "14",
            "name": "Playstation 3",
            "logo_path": "/images/ps3.jpg",
            "tag_name": "nick#4",
            "games": make_game_data()
        }
    ]
    return data


def make_post_mock_data():
    payload = {
        "name": "Brazucas",
        "captain": "1235",
        "members": ["pl11"],
        "consoles": make_console_data(),
        "games": make_game_data()
    }
    return payload


def make_put_mock_data():
    payload = {
        "team_id": "b1e9c0a7",
        "name": "DoRio",
        "captain": "123",
        "members": ["pl11"],
        "consoles": make_console_data(),
        "games": make_game_data()
    }
    return payload


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
def test_get_all_teams_not_found(mock):
    result = get_all_teams()
    assert result.body['message'] == 'Nenhum time encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run')
def test_get_team(mock):
    result = get_team_by_id()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run',
       MagicMock(return_value=None))
def test_get_team_not_found():
    result = get_team_by_id()
    assert result.body['message'] == 'Time não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUser.run')
def test_get_team_by_user(mock):
    result = get_all_teams_by_user()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUser.run',
       MagicMock(return_value=None))
def test_get_teams_by_user_not_found():
    result = get_all_teams_by_user()
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
def test_put_team(mock):
    result = put_team('id1')
    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.team_route.PutTeamInteractor.run',
       MagicMock(side_effect=UpdateTeamException('oops')))
def test_put_team_raises():
    result = put_team('id1')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
