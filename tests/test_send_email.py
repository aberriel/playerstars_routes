from unittest.mock import patch, MagicMock
from chalicelib.send_email import post_email
import json
from tests.test_utils import jwt
import pytest


def make_post_mock_data():
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
@patch('chalicelib.send_email.bp_email', make_post_mock_data())
@patch('chalicelib.send_email.get_player_by_id',
       MagicMock(body=dict(status='success', data='player mock'),
                 status_code=200))
@patch('chalicelib.send_email.SendMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email(client, resource, run):
    result = post_email()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.send_email.bp_email', make_post_mock_data())
@patch('chalicelib.send_email.get_player_by_id',
       MagicMock(body=dict(status='success', data='player mock'),
                 status_code=200))
@patch('chalicelib.send_email.SendMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email_raises(client, resource):
    result = post_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500

# noinspection PyUnusedLocal
@patch('chalicelib.send_email.bp_email', make_post_mock_data())
# @patch('chalicelib.send_email.get_player_by_id',
#        MagicMock(body=dict(status='success', data='player mock'),
#                  status_code=200))
@patch('chalicelib.send_email.SendMailInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email_player_not_found(resource, createtable, save):
    with pytest.raises(BaseException) as excinfo:
        post_email()
    assert str(excinfo.value) == 'Player não encontrado'
