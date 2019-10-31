from chalicelib import (
    championship_route
)
from playerstars_interactors import (
    AcceptInvitationException,
    InvitationNotFoundException
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch

import json


def make_accept_invitation_mock_data():
    payload = """{ "invitation_code": "123" }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


@patch('chalicelib.championship_route.bp_championship',
       make_accept_invitation_mock_data())
@patch('chalicelib.championship_route.AcceptInvitationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_invitation(boto_client,
                                boto_resource,
                                run):
    result = accept_championship_invitation()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


@patch('chalicelib.championship_route.bp_championship',
       make_accept_invitation_mock_data())
@patch('chalicelib.championship_route.AcceptInvitationInteractor.run',
       MagicMock(side_effect=AcceptInvitationException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_invitation_raises(client, resource):
    result = accept_championship_invitation()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
