from chalice_support import server_error, success
from chalicelib.tournament.post_new_invite import tournament_route
from playerstars_interactors.tournament.post_tournament_start import (
    PostTournamentStartAdapters, PostTournamentStartRequestModel,
    PostTournamentStartInteractor, PostTournamentStartError
)
from chalicelib.utils import get_user_id_from_jwt
from playerstars_domain import DuelMemberType as MemmberType
from chalicelib.duel_route_adapters import \
    get_player_adapter, get_team_adapter, get_duel_adapter_dynamo, get_console_adapter
from chalicelib.tournament.get_tournament_detail import (
    get_player_tournament_adapter, get_team_tournament_adapter
)
from chalicelib.tournament.post_tournament import _get_notification_gql_adapter
from chalicelib.settings import Settings


@tournament_route.post('/start/{entity_id}')
def post_tournament_start(entity_id):
    try:
        data = tournament_route.current_request.json_body if tournament_route.current_request else {}
        data.update({'tournament_id': entity_id})
        player_id = get_user_id_from_jwt(tournament_route)
        request = PostTournamentStartRequestModel(
            player_id=player_id,
            member_type=MemmberType.PLAYER,
            data=data
        )
        adapters = PostTournamentStartAdapters(
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            player_tournament_adapter=get_player_tournament_adapter(),
            team_tournament_adapter=get_team_tournament_adapter(),
            notificationgql_adapter=_get_notification_gql_adapter(),
            duel_adapter=get_duel_adapter_dynamo(),
            console_adapter=get_console_adapter()
        )
        interactor = PostTournamentStartInteractor(
            request=request, adapters=adapters,
            time_to_finish=Settings.TIME_TO_FINISH_DUEL)
        response = interactor.run()
        if response:
            return success(response())
        msg = 'Empty response error in post tournament start'
        return server_error(msg)
    except PostTournamentStartError as e:
        msg = "Known error in post tournament start: " + str(e)
        return server_error(msg)
    except BaseException as e:
        msg = "Unknown error in post tournament start: " + str(e)
        return server_error(msg)
