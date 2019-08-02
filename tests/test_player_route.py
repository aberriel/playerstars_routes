#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch
from playerstars_routes import (player_registration)
from playerstars_interactors import PlayerRegistrationException

import json


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
        "consoles": [
            {
                "name": "PS 4",
                "logo_path": "/images/ps4.png",
                "nickname": "007"
            },
            {
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "nickname": "mario"
            }
        ]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.PlayerRegistrationInteractor.run')
def test_player_registration(mock):
    result = player_registration()
    mock.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.player_route.PlayerRegistrationInteractor.run',
       MagicMock(side_effect=PlayerRegistrationException('oops')))
def test_player_registration_raises():
    result = player_registration()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
