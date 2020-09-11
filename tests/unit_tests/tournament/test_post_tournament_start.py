from playerstars_interactors.tournament.post_tournament_start import (
    PostTournamentStartError
)
from chalicelib.tournament.post_tournament_start import (
    post_tournament_start
)
from unittest.mock import MagicMock, patch


@patch('chalicelib.tournament.post_tournament_start.'
       'PostTournamentStartInteractor.run', return_value=(MagicMock()))
@patch('chalicelib.tournament.post_tournament_start.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_tournament_start(client, resource, id, run):
    result = post_tournament_start('schrubles')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


@patch('chalicelib.tournament.post_tournament_start.'
       'PostTournamentStartInteractor.run', side_effect=BaseException('oops'))
@patch('chalicelib.tournament.post_tournament_start.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_tournament_start_error(client, resource, id, run):
    result = post_tournament_start('schrubles')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Unknown error in post tournament start: oops'


@patch('chalicelib.tournament.post_tournament_start.'
       'PostTournamentStartInteractor.run',
       side_effect=PostTournamentStartError('oops'))
@patch('chalicelib.tournament.post_tournament_start.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_tournament_start_known_error(client, resource, id, run):
    result = post_tournament_start('schrubles')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == \
        'Known error in post tournament start: oops'


@patch('chalicelib.tournament.post_tournament_start.'
       'PostTournamentStartInteractor.run', return_value=None)
@patch('chalicelib.tournament.post_tournament_start.get_user_id_from_jwt',
       return_value='id123')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_tournament_start_empty(client, resource, id, run):
    result = post_tournament_start('schrubles')
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'Empty response error in post ' \
                                     'tournament start'
