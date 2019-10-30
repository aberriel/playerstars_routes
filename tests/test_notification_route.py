from playerstars_interactors import \
    SaveEntityException
from chalicelib import post_app_notification
import json
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch


def make_post_mock_data():
    payload = """{
        "player_id": "idteste123",
        "duel_id": "id123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.notification_route.bp_notification', make_post_mock_data())
@patch('chalicelib.notification_route.PostAppNotificationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_app_notification(client, resource, run):
    result = post_app_notification()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.notification_route.bp_notification', make_post_mock_data())
@patch('chalicelib.notification_route.PostAppNotificationInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player_raises(client, resource):
    result = post_app_notification()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
