from playerstars_interactors import \
    PostPurchaseException, PagSeguroException
from chalicelib.pagseguro_purchase_route import (
    post_purchase, post_notification, get_history_route
)
from tests.unit_tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


def make_post_mock_data():
    payload = """{
        "price" : "999",
        "description": "Teste playerstar",
        "product_id": "id123",
        "star_value": 5,
        "star_type": "gold",
        "duration": 0
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_post_mock_data())
@patch('chalicelib.pagseguro_purchase_route.PostPurchaseInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_purchase(client, resource, run):
    result = post_purchase()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_post_mock_data())
@patch('chalicelib.pagseguro_purchase_route.PostPurchaseInteractor.run',
       MagicMock(side_effect=PostPurchaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_purchase_raises(client, resource):
    result = post_purchase()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_noti_mock_data():
    return MagicMock(current_request=MagicMock(
        raw_body=b'notificationType=transaction&notificationCode=A2CDE'))


# noinspection PyUnusedLocal
@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_post_noti_mock_data())
@patch('chalicelib.pagseguro_purchase_route.PostNotificationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_notification(client, resource, run):
    result = post_notification()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_post_noti_mock_data())
@patch('chalicelib.pagseguro_purchase_route.PostNotificationInteractor.run',
       MagicMock(side_effect=PagSeguroException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_notification_raises(client, resource):
    result = post_notification()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_history_mock_data():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_get_history_mock_data())
@patch('chalicelib.pagseguro_purchase_route.GetPurchaseHistoryInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_purchase_history_route(client, resource, run):
    result = get_history_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.pagseguro_purchase_route.bp_purchase',
       make_get_history_mock_data())
@patch('chalicelib.pagseguro_purchase_route.GetPurchaseHistoryInteractor.run',
       return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_purchase_history_route_raises(client, resource, run):
    result = get_history_route()
    assert "Histórico de compras do player" in result.body['message']
    assert result.body['status'] == "error"
    assert result.status_code == 404
