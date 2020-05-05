from chalicelib import (
    get_app_notification,
    get_app_notification_by_status,
    post_app_notification,
    post_set_notification_as_read
)
from playerstars_adapters import NotificationAdapter
from playerstars_interactors import (
    SetNotificationAsReadException,
    SaveEntityException
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


def make_post_mock_data():
    payload = """{
        "duel_id": "id123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


def make_post_set_as_read():
    payload = """{
        "notification_id": "notification123"
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
def test_post_notification_raises(client, resource):
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
    assert "No notifications found" in result.body['message']
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch.object(NotificationAdapter, 'filter', return_value=MagicMock())
@patch('chalicelib.notification_route.bp_notification',
       make_get_app_notification_request())
@patch('chalicelib.notification_route.GetAppNotificationByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_app_notification_by_status(client, resource, run, get_by_id):
    result = get_app_notification_by_status('Closed')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.notification_route.bp_notification_read',
       make_post_set_as_read())
@patch('chalicelib.notification_route.SetNotificationAsReadInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_set_notification_as_read(client, resource, run):
    result = post_set_notification_as_read()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.notification_route.bp_notification_read',
       make_post_set_as_read())
@patch('chalicelib.notification_route.SetNotificationAsReadInteractor.run',
       MagicMock(side_effect=SetNotificationAsReadException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_set_notification_as_read_raises(client, resource):
    result = post_set_notification_as_read()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
