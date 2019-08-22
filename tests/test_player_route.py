#!/usr/bin/env python
# -*- coding: utf-8 -*-

from playerstars_interactors import SavePlayerException
from playerstars_routes import (
    get_all_player,
    get_player_by_id,
    PlayerRoute,
    post_player
)
from unittest.mock import MagicMock, patch

import json
import pytest


def make_post_mock_data():
    payload = """{
        "name": "Anselmo Lira",
        "nickname": "anselmo.lira",
        "birth_date": "16/12/1986",
        "cpf": "123.456.789-00",
        "email": "playerstars@playerstars.com.br",
        "phone_number": "(21) 99663-6963",
        "street": "Rua José de Figueiredo",
        "street_number": "192",
        "street_complement": "Blocos 29, 30",
        "neighborhood": "Barra da Tijuca",
        "city": "Rio de Janeiro",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "postal_code": "22333-000",
        "promo_code": "ABC123",
        "profile_image": "ACCBB4762CF23AA35690CC",
        "favorites":[],
        "blue_star_balance":123,
        "golden_star_balance":  4321,
        "consoles": [
            {
                "entity_id": "1",
                "name": "PS 4",
                "logo_path": "/images/ps4.png",
                "tag_name": "007"
            },
            {
                "entity_id": "11",
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "tag_name": "mario",
                "games": []
            }
        ]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.PostPlayerInteractor.run')
def test_post_player(mock):
    result = post_player()
    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.PostPlayerInteractor.run',
       MagicMock(side_effect=SavePlayerException('oops')))
def test_post_player_raises():
    result = post_player()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.GetPlayerInteractor.run')
def test_get_player(mock):
    result = get_player_by_id('id1')
    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.GetPlayerInteractor.run',
       return_value=None)
def test_get_player_raises(mock):
    result = get_player_by_id('id1')
    mock.assert_called_once()
    assert result.body['message'] == "Player não encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.GetAllPlayersInteractor.run')
def test_get_all_player(mock):
    result = get_all_player()
    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.GetAllPlayersInteractor.run',
       return_value=None)
def test_get_all_player_raises(mock):
    result = get_all_player()
    mock.assert_called_once()
    assert result.body['message'] == "Nenhum player encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        PlayerRoute().make_put_request({})
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        PlayerRoute().update_exception()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        PlayerRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        PlayerRoute().delete_interactor()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        PlayerRoute().put_interactor()
    assert str(exc.value) == 'Não implementado no interactor'
    assert PlayerRoute().delete_not_found() == 'Player não encontrado para' \
                                               ' ser deletado'
