from playerstars_interactors.tournament.post_invite_new_players import (
    PostInviteNewPlayersError
)
from chalicelib.tournament.post_new_invite import (
    post_new_invite
)
from unittest.mock import MagicMock, patch


@patch('chalicelib.tournament.post_new_invite.tournament_route',
       return_value=MagicMock(current_request=MagicMock(json_body=dict(
           tournament_id='tourney123',
           new_players=['glublugb', 'glaabglab']))))
@patch('chalicelib.tournament.post_new_invite.'
       'PostInviteNewPlayersInteractor.run', return_value=(MagicMock()))
@patch('chalicelib.tournament.post_new_invite.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_new_invite(client, resource, id, run, route):
    result = post_new_invite()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.tournament.post_new_invite.tournament_route',
       return_value=MagicMock(current_request=MagicMock(json_body=dict(
           tournament_id='tourney123',
           new_players=['glublugb', 'glaabglab']))))
@patch('chalicelib.tournament.post_new_invite.'
       'PostInviteNewPlayersInteractor.run', side_effect=BaseException('oops'))
@patch('chalicelib.tournament.post_new_invite.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_new_invite_error(client, resource, id, run, route):
    result = post_new_invite()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Unknown error in post new invites: oops'


@patch('chalicelib.tournament.post_new_invite.tournament_route',
       return_value=MagicMock(current_request=MagicMock(json_body=dict(
           tournament_id='tourney123',
           new_players=['glublugb', 'glaabglab']))))
@patch('chalicelib.tournament.post_new_invite.'
       'PostInviteNewPlayersInteractor.run',
       side_effect=PostInviteNewPlayersError('oops'))
@patch('chalicelib.tournament.post_new_invite.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_new_invite_known_error(client, resource, id, run, route):
    result = post_new_invite()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Known error in post new invites: oops'


@patch('chalicelib.tournament.post_new_invite.tournament_route',
       return_value=MagicMock(current_request=MagicMock(json_body=dict(
           tournament_id='tourney123',
           new_players=['glublugb', 'glaabglab']))))
@patch('chalicelib.tournament.post_new_invite.'
       'PostInviteNewPlayersInteractor.run', return_value=None)
@patch('chalicelib.tournament.post_new_invite.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_new_invite_empty(client, resource, id, run, route):
    result = post_new_invite()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'Empty response error in post ' \
                                     'new invites'
