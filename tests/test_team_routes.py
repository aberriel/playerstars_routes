#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_routes import (
    get_all_teams,
    get_team,
    get_team_by_user,
    post_team,
    put_team
)
from unittest.mock import MagicMock, patch

import json
import pytest


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
def test_all_teams_not_found(mock):
    result = get_all_teams()
    assert result.body['message'] == 'Nenhum time encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run')
def test_team(mock):
    result = get_team()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamInteractor.run',
       MagicMock(return_value=None))
def test_team_not_found():
    result = get_team()
    assert result.body['message'] == 'Time não encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUser.run')
def test_get_team_by_user(mock):
    result = get_team_by_user()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.team_route.GetTeamByUser.run',
       MagicMock(return_value=None))
def test_get_teams_by_user_not_found():
    result = get_team_by_user()
    assert result.body['message'] == 'O jogador não possui times'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
def test_post_team():
    pass


# noinspection PyUnusedLocal
def test_post_team_raises():
    pass


# noinspection PyUnusedLocal
def test_put_team():
    pass


# noinspection PyUnusedLocal
def test_put_team_raises():
    pass
