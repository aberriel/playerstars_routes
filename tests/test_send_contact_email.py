from chalicelib.send_contact_email import post_contact_email
from tests.test_utils import jwt
from unittest.mock import patch, MagicMock

import json


def make_post_mock_data():
    payload = """{
        "recipients":["teste@teste.com.br"],
        "template": "teste",
        "sender": "teste@teste.com.br",
        "subject": "testinho",
        "contact_message": "Mensagem de teste",
        "data": ""
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(
            json_body=data,
            headers=dict(AUTHORIZATION=jwt)))


player = {
    "player_status": "OFFLINE",
    "golden_star_balance": 0,
    "purchases": [
        {
            "value": 1050,
            "purchase_datetime": "2017-11-21T09:58:00+00:00",
            "purchase_type": "GOLDEN_STAR_PURCHASE",
            "star_value": 3,
            "payment": {
                "payment_datetime": "2017-11-22T09:58:00+00:00",
                "payment_type": "PAGSEGURO",
                "code": "schrubles123"
            }
        }
    ],
    "entity_id": "acbf5816-3a14-4bf1-a0d3-19efda0151d0",
    "favorites": [
        "ght232141-3a12-5t67-19ehdufasuu"
    ],
    "states_regions": [
        {
            "states": [
                "RJ",
                "MG",
                "SP"
            ],
            "name": "Sudeste",
            "entity_id": "id123",
            "minimum_bet": 123
        }
    ],
    "consoles": [
        {
            "name": "Playstation 4",
            "entity_id": "1",
            "logo_path": "/images/ss.png",
            "games": [],
            "tag_name": "Leoplay4"
        }
    ],
    "user": {
        "date_birth": "2019-09-13",
        "address": "Rua pablin 2, Quadra 3 - Guaratiba",
        "name": "Dada",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "nickname": "leobarnaud",
        "postal_code": "23575275",
        "cpf": "09022715043",
        "profile_image": 'asiuahdiuahsiuasia',
        "country": "Brasil",
        "phone_number": "11111111111",
        "email": "wapilejig@mail-guru.net"
    },
    "blue_star_balance": 15,
    "points": 100,
    "countries_regions": [
        {
            "countries": [
                "EUA",
                "Mexico",
                "Canada"
            ],
            "name": "NA",
            "entity_id": "id123",
            "minimum_bet": 1234
        }
    ],
    "star_transactions": [
        {
            "value": 2,
            "operation_type": "DEBIT",
            "operation_date": "2019-08-21T13:11:07+00:00",
            "coin_type": "GOLDEN_STAR",
            "source": "DUEL",
            "source_id": "68dc45c5-43eb-4351-bead-4319aba7af85"
        }
    ]
}


# noinspection PyUnusedLocal
@patch('chalicelib.send_contact_email.bp_contact_email', make_post_mock_data())
@patch('chalicelib.send_contact_email.get_player_by_id',
       MagicMock(body=dict(status='success', data=player),
                 status_code=200))
@patch('chalicelib.send_contact_email.SendContactMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email(client, resource, run):
    result = post_contact_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.send_contact_email.bp_contact_email', make_post_mock_data())
@patch('chalicelib.send_contact_email.get_player_by_id',
       MagicMock(body=dict(status='success', data=player),
                 status_code=200))
@patch('chalicelib.send_contact_email.SendContactMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email_raises(client, resource):
    result = post_contact_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
