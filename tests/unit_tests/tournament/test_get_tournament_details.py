from playerstars_interactors.tournament.get_tournament_detail import (
    GetTournamentError
)
from chalicelib.tournament.get_tournament_detail import (
    get_tournament_details
)
from unittest.mock import MagicMock, patch
from tests.unit_tests.test_utils import jwt


@patch('chalicelib.tournament.get_tournament_detail.tournament_route',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.tournament.get_tournament_detail.'
       'GetTournamentInteractor.run', return_value=(MagicMock()))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_tournaments(client, resource, run):
    result = get_tournament_details('tournament123')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.tournament.get_tournament_detail.tournament_route',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.tournament.get_tournament_detail.'
       'GetTournamentInteractor.run', side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_tournaments_error(client, resource, run):
    result = get_tournament_details('tournamente123')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Unknown error getting tournament details: oops'


# noinspection PyUnusedLocal
@patch('chalicelib.tournament.get_tournament_detail.tournament_route',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.tournament.get_tournament_detail.'
       'GetTournamentInteractor.run', side_effect=GetTournamentError('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_tournaments_known_error(client, resource, run):
    result = get_tournament_details('tournamente123')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Known error getting tournament details: oops'


# noinspection PyUnusedLocal
@patch('chalicelib.tournament.get_tournament_detail.tournament_route',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.tournament.get_tournament_detail.'
       'GetTournamentInteractor.run', return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_tournaments_not_found(client, resource, run):
    result = get_tournament_details('tournament123')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert result.body['message'] == \
        'Tournament tournament123 not found for the player' \
        ' 8ad1635f-2263-4dda-879a-bd24b5d9732f'
