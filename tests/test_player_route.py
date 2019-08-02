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
                "tag_name": "007"
            },
            {
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "tag_name": "mario"
            }
        ]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
def test_player_registration():
    pass


# noinspection PyUnusedLocal
def test_player_registration_raises():
    pass
