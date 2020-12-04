from chalicelib import (
    get_app_notification,
    get_app_notification_by_status,
    post_app_notification,
    post_set_notification_as_read,
    post_player_sns_token)
from playerstars_adapters import NotificationAdapter
from playerstars_interactors import (
    SetNotificationAsReadException,
    SaveEntityException)
from playerstars_interactors.notification import PostPlayerSnsEndpointException
from tests.unit_tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


prefix = 'chalicelib.notification_route'


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
@patch(f'{prefix}.bp_notification', make_post_mock_data())
@patch(f'{prefix}.PostAppNotificationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_app_notification(client, resource, run):
    result = post_app_notification()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch(f'{prefix}.bp_notification', make_post_mock_data())
@patch(f'{prefix}.PostAppNotificationInteractor.run',
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
@patch(f'{prefix}.bp_notification',
       make_get_app_notification_request())
@patch(f'{prefix}.GetAppNotificationByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_app_notification(client, resource, run, get_by_id):
    result = get_app_notification()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch.object(NotificationAdapter, 'filter', return_value=MagicMock())
@patch(f'{prefix}.bp_notification',
       make_get_app_notification_request())
@patch(f'{prefix}.GetAppNotificationByUserInteractor.run',
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
@patch(f'{prefix}.bp_notification',
       make_get_app_notification_request())
@patch(f'{prefix}.GetAppNotificationByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_app_notification_by_status(client, resource, run, get_by_id):
    result = get_app_notification_by_status('Closed')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch(f'{prefix}.bp_notification_read',
       make_post_set_as_read())
@patch(f'{prefix}.SetNotificationAsReadInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_set_notification_as_read(client, resource, run):
    result = post_set_notification_as_read()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch(f'{prefix}.bp_notification_read',
       make_post_set_as_read())
@patch(f'{prefix}.SetNotificationAsReadInteractor.run',
       MagicMock(side_effect=SetNotificationAsReadException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_set_notification_as_read_raises(client, resource):
    result = post_set_notification_as_read()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


@patch(f'{prefix}.PostPlayerSnsEndpointRequestModel')
@patch(f'{prefix}.PostPlayerSnsEndpointInteractor')
@patch(f'{prefix}.get_user_id_from_jwt')
@patch(f'{prefix}.success')
@patch(f'{prefix}.server_error')
@patch(f'{prefix}.bp_notification')
@patch(f'{prefix}.Settings')
@patch(f'{prefix}.get_player_adapter')
def test_post_player_sns_token(mock_get_player_adapter,
                               mock_settings,
                               mock_bp_notification,
                               mock_server_error,
                               mock_success,
                               mock_get_user_id_from_jwt,
                               mock_interactor,
                               mock_request_model):
    response = post_player_sns_token()
    mock_get_user_id_from_jwt.assert_called_with(mock_bp_notification)
    mock_bp_notification.current_request.json_body.update.assert_called_with(
        {'player_id': mock_get_user_id_from_jwt()})
    mock_request_model.assert_called_with(
        mock_bp_notification.current_request.json_body)
    mock_get_player_adapter.assert_called()
    mock_interactor.assert_called_with(
        request=mock_request_model(),
        player_adapter=mock_get_player_adapter(),
        platform_arn=mock_settings.ANDROID_PUSH_NOTIFICATION_PLATFORM_ARN,
        aws_region=mock_settings.AWS_DEFAULT_REGION)
    mock_interactor().run.assert_called()
    mock_server_error.assert_not_called()
    mock_success.assert_called_with(mock_interactor().run()())
    assert response == mock_success()


@patch(f'{prefix}.PostPlayerSnsEndpointRequestModel')
@patch(f'{prefix}.PostPlayerSnsEndpointInteractor.run',
       side_effect=PostPlayerSnsEndpointException('oops'))
@patch(f'{prefix}.get_user_id_from_jwt')
@patch(f'{prefix}.bp_notification')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player_sns_token_error(boto_client,
                                     boto_resource,
                                     mock_bp_notification,
                                     mock_get_user_id_from_jwt,
                                     mock_run,
                                     mock_request_model):
    result = post_player_sns_token()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
