from unittest.mock import patch, MagicMock
from chalicelib.send_email import post_email
import json


def make_post_mock_data():
    payload = """{
        "recipients":["teste@teste.com.br"],
        "data": ""
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.send_email.bp_email', make_post_mock_data())
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
@patch('chalicelib.send_email.SendMailInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_email_raises(client, resource):
    result = post_email()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
