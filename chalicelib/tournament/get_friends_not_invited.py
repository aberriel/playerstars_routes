from chalice_support import not_found, server_error, success
from chalicelib.utils import get_user_id_from_jwt
from chalicelib.tournament.post_invite_answer import (
    tournament_route, get_player_tournament_adapter, get_player_adapter)
from chalicelib.player_route import get_console_adapter
from playerstars_interactors.tournament.get_friends_not_invited import (
    GetFriendsNotInvitedAdapters, GetFriendsNotInvitedInteractor,
    GetFriendsNotInvitedRequestModel, GetFriendsNotInvitedError
)


@tournament_route.get('/friends-not-invited/')
def get_friends_not_invited_route():
    try:
        data = tournament_route.current_request.query_params
        entity_id = get_user_id_from_jwt(tournament_route)
        request = GetFriendsNotInvitedRequestModel(
            player_id=entity_id,
            tournament_id=data.get('tournament_id'))
        adapters = GetFriendsNotInvitedAdapters(
            player_adapter=get_player_adapter(),
            console_adapter=get_console_adapter(),
            player_tournament_adapter=get_player_tournament_adapter()
        )
        interactor = GetFriendsNotInvitedInteractor(
            request=request,
            adapters=adapters)
        response = interactor.run()
        if response:
            return success(response())
        return not_found(f"Nenhum amigo do player {entity_id} encontrado para"
                         f" o campeonato {data.get('tournament_id')}")
    except GetFriendsNotInvitedError as e:
        msg = f"Known error getting friends for tournament. {str(e)}"
        return server_error(msg)
    except BaseException as e:
        msg = f"Unknown error getting friends for tournament. {str(e)}"
        return server_error(msg)
