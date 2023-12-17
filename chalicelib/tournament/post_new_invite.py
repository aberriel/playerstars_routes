from chalice_support import server_error, success
from chalicelib.tournament.get_friends_not_invited import tournament_route
from playerstars_interactors.tournament.post_invite_new_players import (
    PostInviteNewPlayersAdapters, PostInviteNewPlayersRequestModel,
    PostInviteNewPlayersInteractor, PostInviteNewPlayersError)
from chalicelib.utils import get_user_id_from_jwt
from playerstars_domain import DuelMemberType as MemmberType
from chalicelib.duel_route_adapters import get_player_adapter, get_team_adapter
from chalicelib.tournament.get_tournament_detail import get_player_tournament_adapter, get_team_tournament_adapter
from chalicelib.tournament.post_tournament import _get_notification_gql_adapter


@tournament_route.post('/invite/')
def post_new_invite():
    try:
        data = tournament_route.current_request.json_body
        player_id = get_user_id_from_jwt(tournament_route)
        request = PostInviteNewPlayersRequestModel(player_id=player_id, member_type=MemmberType.PLAYER, data=data)
        adapters = PostInviteNewPlayersAdapters(
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            player_tournament_adapter=get_player_tournament_adapter(),
            team_tournament_adapter=get_team_tournament_adapter(),
            notification_gql=_get_notification_gql_adapter()
        )
        interactor = PostInviteNewPlayersInteractor(request=request, adapters=adapters)
        response = interactor.run()
        if response:
            return success(response())
        msg = 'Empty response error in post new invites'
        return server_error(msg)
    except PostInviteNewPlayersError as e:
        msg = "Known error in post new invites: " + str(e)
        return server_error(msg)
    except BaseException as e:
        msg = "Unknown error in post new invites: " + str(e)
        return server_error(msg)
