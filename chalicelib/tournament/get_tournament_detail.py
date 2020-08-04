from chalice_support import (not_found, server_error, success)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from chalicelib.tournament.post_tournament import tournament_route
from playerstars_interactors.tournament.get_tournament_detail import (
    GetTournamentInteractor, GetTournamentRequestModel, GetTournamentError,
    GetTournamentAdapters
)
from chalicelib.duel_route_adapters import \
    get_player_adapter, get_team_adapter
from playerstars_adapters import \
    PlayerTournamentAdapter, TeamTournamentAdapter


def get_player_tournament_adapter():
    return PlayerTournamentAdapter(
        Settings.PLAYER_TOURNAMENT_TABLE_NAME, Settings.DYNAMODB_URL)


def get_team_tournament_adapter():
    return TeamTournamentAdapter(
        Settings.TEAM_TOURNAMENT_TABLE_NAME, Settings.DYNAMODB_URL)


@tournament_route.get('/{entity_id}')
def get_tournament_details(entity_id):
    try:
        player_id = get_user_id_from_jwt(tournament_route)
        request = GetTournamentRequestModel(
            tournament_id=entity_id, player_id=player_id)
        adapters = GetTournamentAdapters(
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            player_tournament_adapter=get_player_tournament_adapter(),
            team_tournament_adapter=get_team_tournament_adapter()
        )
        interactor = GetTournamentInteractor(
            request=request,
            adapters=adapters,
            tournament_review_time=Settings.TOURNAMENT_REVIEW_TIME)
        response = interactor.run()
        if response:
            return success(response())
        return not_found(
            f"Tournament {entity_id} not found for the player {player_id}")
    except GetTournamentError as e:
        msg = "Known error getting tournament details: " + str(e)
        return server_error(msg)
    except BaseException as e:
        msg = "Unknown error getting tournament details: " + str(e)
        return server_error(msg)
