from chalicelib import (
    get_all_championships,
    get_championship_by_id,
    post_accept_invitation,
    post_add_friend_to_championship,
    post_create_championship,
    post_join_open_championship
)
from playerstars_interactors import (
    AcceptInvitationException,
    AddFriendToChampionshipException,
    CreateChampionshipException,
    JoinOpenChampionshipException
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


def make_accept_invitation_mock_data():
    payload = """{
        "invitation_code": "123",
        "accepted": true
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


def make_add_friend_to_championship_mock_data():
    payload = """{
        "request_member_id": "123",
        "member_type": "Player",
        "friend_id": "456",
        "championship_id": "abc"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)
    ))


def make_create_championship_mock_data():
    payload = """{
        "name": "Brazucas",
        "game": {
            "entity_id": "aq1w2e3",
            "name": "Sonic",
            "logo_path": "/images/sonic.jpg"
        },
        "console": {
            "entity_id": "a1s2d3",
            "name": "Master System",
            "logo_path": "/images/master_system.jpg",
            "games": {
                "entity_id": "q1w2e3",
                "name": "Sonic",
                "logo_path": "/images/sonic.jpg"
            }
        },
        "owner": "13256",
        "is_open": true,
        "price_to_enter": 3,
        "members": ["tuv76", "akk65"],
        "championship_type": "Player",
        "max_members": 4,
        "start_datetime": "2019-12-10T13:25:07+00:00"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


def make_join_open_championship_mock_data():
    payload = """{
        "member_id": "a1b2c3",
        "member_type": "Player",
        "championship_id": "qwe123"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.GetAllChampionshipsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_championships(client, resource, run):
    result = get_all_championships()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.GetAllChampionshipsInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_championships_empty(client, resource):
    result = get_all_championships()
    assert result.body['message'] == 'No championship found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.GetAllChampionshipsInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_championship_raises(client, resource):
    result = get_all_championships()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_accept_invitation',
       make_accept_invitation_mock_data())
@patch('chalicelib.championship_route.AcceptInvitationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_invitation(boto_client,
                                boto_resource,
                                run):
    result = post_accept_invitation()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_accept_invitation',
       make_accept_invitation_mock_data())
@patch('chalicelib.championship_route.AcceptInvitationInteractor.run',
       MagicMock(side_effect=AcceptInvitationException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_invitation_raises(client, resource):
    result = post_accept_invitation()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_create_championship',
       make_create_championship_mock_data())
@patch('chalicelib.championship_route.CreateChampionshipInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_create_championship(boto_client,
                                  boto_resource,
                                  run):
    result = post_create_championship()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_create_championship',
       make_create_championship_mock_data())
@patch('chalicelib.championship_route.CreateChampionshipInteractor.run',
       MagicMock(side_effect=CreateChampionshipException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_create_championship_raises(boto_client,
                                         boto_resource):
    result = post_create_championship()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_join_open_championship',
       make_join_open_championship_mock_data())
@patch('chalicelib.championship_route.JoinOpenChampionshipInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_join_open_championship(boto_client,
                                     boto_resource,
                                     run):
    result = post_join_open_championship()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_join_open_championship',
       make_join_open_championship_mock_data())
@patch('chalicelib.championship_route.JoinOpenChampionshipInteractor.run',
       MagicMock(side_effect=JoinOpenChampionshipException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_join_open_championship_raises(boto_client,
                                            boto_resource):
    result = post_join_open_championship()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_add_friend_to_championship',
       make_add_friend_to_championship_mock_data())
@patch('chalicelib.championship_route.AddFriendToChampionshipInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_add_friend_to_championship(boto_client,
                                         boto_resource,
                                         run):
    result = post_add_friend_to_championship()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.championship_route.bp_add_friend_to_championship',
       make_add_friend_to_championship_mock_data())
@patch('chalicelib.championship_route.AddFriendToChampionshipInteractor.run',
       MagicMock(side_effect=AddFriendToChampionshipException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_add_friend_to_championship_raises(boto_client,
                                                boto_resource):
    result = post_add_friend_to_championship()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
