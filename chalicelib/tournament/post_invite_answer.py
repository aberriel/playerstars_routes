from chalice_support import server_error, success
from chalicelib.tournament.get_tournament_detail import tournament_route
from playerstars_interactors.tournament.post_invite_answer import (
    PostInviteAnswerError, PostInviteAnswerRequestModel,
    PostInviteAnswerInteractor, PostInviteAnswerAdapters
)
from chalicelib.utils import get_user_id_from_jwt
from playerstars_domain import DuelMemberType as MemmberType
from chalicelib.duel_route_adapters import get_player_adapter, get_team_adapter
from chalicelib.tournament.get_tournament_detail import (
    get_player_tournament_adapter, get_team_tournament_adapter
)


@tournament_route.post('/player/accept/')
def post_accept_invite():
    return invite_answer('ACCEPT', tournament_route)


@tournament_route.post('/player/reject/')
def post_reject_invite():
    return invite_answer('REJECT', tournament_route)


def invite_answer(answer, route):
    try:
        data = route.current_request.json_body
        player_id = get_user_id_from_jwt(route)
        request = PostInviteAnswerRequestModel(
            player_id=player_id,
            member_type=MemmberType.PLAYER,
            data=data,
            answer=answer)
        adapters = PostInviteAnswerAdapters(
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            player_tournament_adapter=get_player_tournament_adapter(),
            team_tournament_adapter=get_team_tournament_adapter())
        interactor = PostInviteAnswerInteractor(request=request, adapters=adapters)
        response = interactor.run()
        if response:
            return success(response())
        msg = 'Empty response error in post answer'
        return server_error(msg)
    except PostInviteAnswerError as e:
        msg = "Known error in post answer: " + str(e)
        return server_error(msg)
    except BaseException as e:
        msg = "Unknown error in post answer: " + str(e)
        return server_error(msg)
