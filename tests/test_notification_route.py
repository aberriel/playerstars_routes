from playerstars_interactors import \
    SaveEntityException
from chalicelib import post_app_notification, get_app_notification
import json
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch
from playerstars_adapters import NotificationAdapter


def make_post_mock_data():
    payload = """{
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


def make_get_app_notification_request():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch.object(NotificationAdapter, 'filter', return_value=MagicMock())
@patch('chalicelib.notification_route.bp_notification',
       make_get_app_notification_request())
@patch('chalicelib.notification_route.GetAppNotificationByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_app_notification(client, resource, run, get_by_id):
    result = get_app_notification()

    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch.object(NotificationAdapter, 'filter', return_value=MagicMock())
@patch('chalicelib.notification_route.bp_notification',
       make_get_app_notification_request())
@patch('chalicelib.notification_route.GetAppNotificationByUserInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_app_notification_raises(client, resource, get_by_id):
    result = get_app_notification()
    assert "Nenhuma notificação encontrada" in result.body['message']
    assert result.body['status'] == "error"
    assert result.status_code == 404
