from chalicelib.tournament.get_friends_not_invited import (
    get_friends_not_invited_route
)
from playerstars_interactors.tournament.get_friends_not_invited import (
    GetFriendsNotInvitedError
)
from unittest.mock import patch, MagicMock
from tests.test_utils import jwt


@patch('chalicelib.tournament.get_friends_not_invited.tournament_route',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           query_param=dict(tournament_id='schrubles123'))))
@patch('chalicelib.tournament.get_friends_not_invited.'
       'GetFriendsNotInvitedInteractor.run', return_value=MagicMock())
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_not_invited_route(mock, mock1, mock2):
    response = get_friends_not_invited_route()
    assert response.body['status'] == 'success'
    assert response.status_code == 200


@patch('chalicelib.tournament.get_friends_not_invited.tournament_route',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           query_param=dict(tournament_id='schrubles123'))))
@patch('chalicelib.tournament.get_friends_not_invited.'
       'GetFriendsNotInvitedInteractor.run', return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_not_invited_route_not_found(mock, mock1, mock2):
    response = get_friends_not_invited_route()
    assert response.body['status'] == 'error'
    assert response.status_code == 404
    assert 'Nenhum amigo do player 8ad1635f-2263-4dda-879a-bd24b5d9732f' \
           ' encontrado para o campeonato' in response.body['message']


@patch('chalicelib.tournament.get_friends_not_invited.tournament_route',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           query_param=dict(tournament_id='schrubles123'))))
@patch('chalicelib.tournament.get_friends_not_invited.'
       'GetFriendsNotInvitedInteractor.run',
       side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_not_invited_route_raises(mock, mock1, mock2):
    response = get_friends_not_invited_route()
    assert response.body['status'] == 'error'
    assert response.status_code == 500
    assert response.body['message'] == \
        'Unknown error getting friends for tournament. oops'


@patch('chalicelib.tournament.get_friends_not_invited.tournament_route',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt),
           query_param=dict(tournament_id='schrubles123'))))
@patch('chalicelib.tournament.get_friends_not_invited.'
       'GetFriendsNotInvitedInteractor.run',
       side_effect=GetFriendsNotInvitedError('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_not_invited_route_raises2(mock, mock1, mock2):
    response = get_friends_not_invited_route()
    assert response.body['status'] == 'error'
    assert response.status_code == 500
    assert response.body['message'] == \
        'Known error getting friends for tournament. oops'
