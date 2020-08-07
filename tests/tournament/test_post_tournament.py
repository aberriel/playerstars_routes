from unittest.mock import patch, MagicMock

from marshmallow import ValidationError
from playerstars_domain import DuelMemberType as MemberType

from chalicelib.settings import Settings


# noinspection PyProtectedMember
from chalicelib.tournament.post_tournament import (
    _get_tournament_adapter,
    _get_console_adapter,
    _get_values_adapter, post_tournament)


@patch('chalicelib.tournament.post_tournament.PlayerTournamentAdapter')
def test_get_tournament_adapter_player(mock_adapter):
    mock_rest_model = MagicMock(duel_type=MemberType.PLAYER)
    result = _get_tournament_adapter(mock_rest_model)

    mock_adapter.assert_called_with(
        table_name=Settings.PLAYER_TOURNAMENT_TABLE_NAME)
    assert result == mock_adapter()


@patch('chalicelib.tournament.post_tournament.TeamTournamentAdapter')
def test_get_tournament_adapter_team(mock_adapter):
    mock_rest_model = MagicMock(duel_type=MemberType.TEAM)
    result = _get_tournament_adapter(mock_rest_model)

    mock_adapter.assert_called_with(
        table_name=Settings.TEAM_TOURNAMENT_TABLE_NAME)
    assert result == mock_adapter()


@patch('chalicelib.tournament.post_tournament.ConsoleAdapter')
def test_get_console_adapter(mock_adapter):
    result = _get_console_adapter()

    mock_adapter.assert_called_with(table_name=Settings.CONSOLE_TABLE_NAME)
    assert result == mock_adapter()


@patch('chalicelib.tournament.post_tournament.ValuesAdapter')
def test_get_values_adapter(mock_adapter):
    result = _get_values_adapter()

    mock_adapter.assert_called_with(table_name=Settings.VALUES_TABLE_NAME)
    assert result == mock_adapter()


@patch('chalicelib.tournament.post_tournament.JwtUtils')
@patch('chalicelib.tournament.post_tournament.tournament_route')
@patch('chalicelib.tournament.post_tournament.PostTournamentRestModel')
@patch('chalicelib.tournament.post_tournament._get_tournament_adapter')
@patch('chalicelib.tournament.post_tournament._get_console_adapter')
@patch('chalicelib.tournament.post_tournament._get_values_adapter')
@patch('chalicelib.tournament.post_tournament._get_notification_gql_adapter')
@patch('chalicelib.tournament.post_tournament.PostTournamentAdapters')
@patch('chalicelib.tournament.post_tournament.PostTournamentInteractor')
@patch('chalicelib.tournament.post_tournament.success')
def test_post_tournament(mock_success,
                         mock_interactor,
                         mock_adapters,
                         mock_get_notification_gql,
                         mock_get_values,
                         mock_get_console,
                         mock_get_tournament,
                         mock_rest_model,
                         mock_bp,
                         mock_ju):
    result = post_tournament()

    mock_ju.assert_called_with(mock_bp)
    mock_ju().get_username_from_jwt.assert_called_once()
    mock_rest_model.from_json.assert_called_with(
        mock_bp.current_request.json_body)
    mock_request = mock_rest_model.from_json()
    mock_get_tournament.assert_called_with(mock_request)
    mock_get_console.assert_called_once()
    mock_get_values.assert_called_once()
    mock_adapters.assert_called_with(
        tournament=mock_get_tournament(),
        console=mock_get_console(),
        values=mock_get_values(),
        notification_gql=mock_get_notification_gql())
    mock_interactor.assert_called_with(
        request=mock_request,
        adapters=mock_adapters(),
        player_id=mock_ju().get_username_from_jwt())
    mock_interactor().run.assert_called_once()
    mock_success.assert_called_with(
        mock_interactor().run().to_json())

    assert result == mock_success()


# noinspection PyUnusedLocal
@patch('chalicelib.tournament.post_tournament.JwtUtils')
@patch('chalicelib.tournament.post_tournament.tournament_route')
@patch('chalicelib.tournament.post_tournament.PostTournamentRestModel',
       from_json=MagicMock(side_effect=ValidationError('Inválido mané!')))
@patch('chalicelib.tournament.post_tournament.bad_request')
def test_post_tournament_bad_request(mock_bad_request,
                                     mock_rest_model,
                                     mock_bp,
                                     mock_ju):
    result = post_tournament()

    mock_bad_request.assert_called_with(
        'Validation Error loading request: Inválido mané!')

    assert result == mock_bad_request()


# noinspection PyUnusedLocal
@patch('chalicelib.tournament.post_tournament.JwtUtils')
@patch('chalicelib.tournament.post_tournament.tournament_route')
@patch('chalicelib.tournament.post_tournament.PostTournamentRestModel')
@patch('chalicelib.tournament.post_tournament._get_tournament_adapter')
@patch('chalicelib.tournament.post_tournament._get_console_adapter')
@patch('chalicelib.tournament.post_tournament._get_values_adapter')
@patch('chalicelib.tournament.post_tournament.PostTournamentAdapters')
@patch('chalicelib.tournament.post_tournament.PostTournamentInteractor',
       return_value=MagicMock(
           run=MagicMock(
               side_effect=ValueError('Deu ruim!'))))
@patch('chalicelib.tournament.post_tournament.server_error')
def test_post_tournament_error(mock_server_error,
                               mock_interactor,
                               mock_adapters,
                               mock_get_values,
                               mock_get_console,
                               mock_get_tournament,
                               mock_rest_model,
                               mock_bp,
                               mock_ju):
    result = post_tournament()
    mock_server_error.assert_called_with('Unknown error posting tournament: '
                                         'ValueError(Deu ruim!)')

    assert result == mock_server_error()
