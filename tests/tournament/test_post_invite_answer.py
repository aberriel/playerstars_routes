from playerstars_interactors.tournament.post_invite_answer import (
    PostInviteAnswerError
)
from chalicelib.tournament.post_invite_answer import (
    post_accept_invite, post_reject_invite, invite_answer
)
from unittest.mock import MagicMock, patch


@patch('chalicelib.tournament.post_invite_answer.'
       'PostInviteAnswerInteractor.run', return_value=(MagicMock()))
@patch('chalicelib.tournament.post_invite_answer.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invite_answer(client, resource, id, run):
    schrubles = MagicMock(current_request=MagicMock(
        json_body=dict(tournament_id='tourney123')))
    result = invite_answer('tournament123', schrubles)
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.tournament.post_invite_answer.'
       'PostInviteAnswerInteractor.run', side_effect=BaseException('oops'))
@patch('chalicelib.tournament.post_invite_answer.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invite_answer_error(client, resource, id, run):
    schrubles = MagicMock(current_request=MagicMock(
        json_body=dict(tournament_id='tourney123')))
    result = invite_answer('tournament123', schrubles)
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Unknown error in post answer: oops'


@patch('chalicelib.tournament.post_invite_answer.'
       'PostInviteAnswerInteractor.run',
       side_effect=PostInviteAnswerError('oops'))
@patch('chalicelib.tournament.post_invite_answer.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invite_answer_known_error(client, resource, id, run):
    schrubles = MagicMock(current_request=MagicMock(
        json_body=dict(tournament_id='tourney123')))
    result = invite_answer('tournament123', schrubles)
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Known error in post answer: oops'


@patch('chalicelib.tournament.post_invite_answer.'
       'PostInviteAnswerInteractor.run', return_value=None)
@patch('chalicelib.tournament.post_invite_answer.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_invite_answer_empty(client, resource, id, run):
    schrubles = MagicMock(current_request=MagicMock(
        json_body=dict(tournament_id='tourney123')))
    result = invite_answer('tournament123', schrubles)
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'Empty response error in post answer'


@patch('chalicelib.tournament.post_invite_answer.invite_answer')
@patch('chalicelib.tournament.post_invite_answer.tournament_route')
def test_post_accept_invite(route, func):
    response = post_accept_invite()
    assert response
    func.assert_called_once_with('ACCEPT', route)


@patch('chalicelib.tournament.post_invite_answer.invite_answer')
@patch('chalicelib.tournament.post_invite_answer.tournament_route')
def test_post_reject_invite(route, func):
    response = post_reject_invite()
    assert response
    func.assert_called_once_with('REJECT', route)
