from chalicelib.mail_routes import (
    post_contact_email, post_welcome_email, post_invitation_email,
    post_public_contact_email)
from tests.unit_tests.test_utils import jwt
from unittest.mock import patch, MagicMock


import json


def contact_email_data():
    payload = {
        'recipients': ['teste@teste.com.br'],
        'template': 'teste',
        'sender': 'teste@teste.com.br',
        'subject': 'testinho',
        'contact_message': 'Mensagem de teste',
        'data': ''
    }
    return MagicMock(
        current_request=MagicMock(
            json_body=payload,
            headers=dict(AUTHORIZATION=jwt)))


player = {
    'player_status': 'OFFLINE',
    'golden_star_balance': 0,
    'purchases': [
        {
            'value': 1050,
            'purchase_datetime': '2017-11-21T09:58:00+00:00',
            'purchase_type': 'GOLDEN_STAR_PURCHASE',
            'star_value': 3,
            'payment': {
                'payment_datetime': '2017-11-22T09:58:00+00:00',
                'payment_type': 'PAGSEGURO',
                'code': 'schrubles123'
            }
        }
    ],
    'entity_id': 'acbf5816-3a14-4bf1-a0d3-19efda0151d0',
    'favorites': ['ght232141-3a12-5t67-19ehdufasuu'],
    'states_regions': ['id123'],
    'consoles': [
        {
            'console_id': 'c01',
            'game_points': [],
            'tag_name': 'Leoplay4'
        }
    ],
    'user': {
        'date_birth': '2019-09-13',
        'address': 'Rua pablin 2, Quadra 3 - Guaratiba',
        'name': 'Dada',
        'city': 'Rio de Janeiro',
        'state': 'RJ',
        'nickname': 'leobarnaud',
        'postal_code': '23575275',
        'cpf': '09022715043',
        'profile_image': 'asiuahdiuahsiuasia',
        'country': 'Brasil',
        'phone_number': '11111111111',
        'email': 'wapilejig@mail-guru.net'
    },
    'blue_star_balance': 15,
    'points': 100,
    'countries_regions': ['id123'],
    'star_transactions': [
        {
            'value': 2,
            'operation_type': 'DEBIT',
            'operation_date': '2019-08-21T13:11:07+00:00',
            'coin_type': 'GOLDEN_STAR',
            'source': 'DUEL',
            'source_id': '68dc45c5-43eb-4351-bead-4319aba7af85'
        }
    ]
}


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_contact_email', contact_email_data())
@patch('chalicelib.mail_routes.SendContactMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_contact_email(client, resource, run):
    result = post_contact_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_contact_email', contact_email_data())
@patch('chalicelib.mail_routes.SendContactMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_contact_email_raises(client, resource):
    result = post_contact_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def public_contact_email_data():
    payload = {
        'recipients': ['teste@teste.com.br'],
        'template': 'teste',
        'sender': 'teste@teste.com.br',
        'subject': 'testinho',
        'contact_message': 'Mensagem de teste',
        'data': '',
        'sender_name': 'schrubles',
        'sender_mail': 'schrubles@ig.com.br'
    }
    return MagicMock(current_request=MagicMock(json_body=payload))


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_contact_email', public_contact_email_data())
@patch('chalicelib.mail_routes.SendContactMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_public_contact_email(client, resource, run):
    result = post_public_contact_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_contact_email', public_contact_email_data())
@patch('chalicelib.mail_routes.SendContactMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_public_contact_email_raises(client, resource):
    result = post_public_contact_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def invitation_mail_data():
    payload = """{
        "recipients":["teste@teste.com.br"],
        "template": "teste",
        "sender": "teste@teste.com.br",
        "subject": "testinho",
        "data": ""
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(
            json_body=data,
            headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_invitation_email',
       invitation_mail_data())
@patch('chalicelib.mail_routes.SendInvitationMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invitation_email(client, resource, run):
    result = post_invitation_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_invitation_email',
       invitation_mail_data())
@patch('chalicelib.mail_routes.SendInvitationMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invitation_email_raises(client, resource):
    result = post_invitation_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def welcome_email_data():
    payload = """{
        "recipients":["teste@teste.com.br"],
        "template": "teste",
        "sender": "teste@teste.com.br",
        "subject": "testinho",
        "data": ""
    }"""
    data = json.loads(payload)
    return MagicMock(
        current_request=MagicMock(
            json_body=data,
            headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_welcome_email', welcome_email_data())
@patch('chalicelib.mail_routes.SendWelcomeMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_welcome_email(client, resource, run):
    result = post_welcome_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.mail_routes.bp_welcome_email', welcome_email_data())
@patch('chalicelib.mail_routes.SendWelcomeMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_welcome_email_raises(client, resource):
    result = post_welcome_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
