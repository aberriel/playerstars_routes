from chalice import Blueprint
from chalicelib.chalice_support import (
    private_post,
    server_error,
    success
)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from playerstars_adapters import (
    ChampionshipAdapter,
    PlayerAdapter,
    TeamAdapter
)
from playerstars_interactors import (
    AcceptInvitationException,
    AcceptInvitationInteractor,
    AcceptInvitationRequestModel,

    AddFriendToChampionshipException,
    AddFriendToChampionshipInteractor,
    AddFriendToChampionshipRequestModel,

    CreateChampionshipException,
    CreateChampionshipRequestModel,
    CreateChampionshipInteractor,

    JoinOpenChampionshipException,
    JoinOpenChampionshipInteractor,
    JoinOpenChampionshipRequestModel
)


bp_accept_invitation = Blueprint(__name__)
bp_add_friend_to_championship = Blueprint(__name__)
bp_create_championship = Blueprint(__name__)
bp_join_open_championship = Blueprint(__name__)


def get_championship_adapter():
    return ChampionshipAdapter(Settings.CHAMPIONSHIP_TABLE_NAME,
                               Settings.DYNAMODB_URL)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_create_championship.route('/', **private_post())
def post_create_championship():
    data = bp_create_championship.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_create_championship)
    data.update({'owner': entity_id})

    player_adapter = get_player_adapter()
    championship_adapter = get_championship_adapter()
    team_adapter = get_team_adapter()

    request = CreateChampionshipRequestModel(data)
    interactor = CreateChampionshipInteractor(
        request=request,
        championship_adapter=championship_adapter,
        player_adapter=player_adapter,
        team_adapter=team_adapter
    )

    try:
        response = interactor.run()
    except CreateChampionshipException as exc:
        return server_error(str(exc))
    return success(response)


@bp_accept_invitation.route('/', **private_post())
def post_accept_invitation():
    data = bp_accept_invitation.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_accept_invitation)
    data.update({'entity_id': entity_id})

    player_adapter = get_player_adapter()
    championship_adapter = get_championship_adapter()
    team_adapter = get_team_adapter()

    request = AcceptInvitationRequestModel(
        invitation_code=data['invitation_code'],
        accepted=data['accepted']
    )
    interactor = AcceptInvitationInteractor(
        request=request,
        player_adapter=player_adapter,
        team_adapter=team_adapter,
        championship_adapter=championship_adapter
    )

    try:
        response = interactor.run()
    except AcceptInvitationException as exc:
        return server_error(str(exc))

    return success(response)


@bp_join_open_championship.route('/', **private_post())
def post_join_open_championship():
    data = bp_join_open_championship.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_join_open_championship)
    data.update({'entity_id': entity_id})

    championship_adapter = get_championship_adapter()
    player_adapter = get_player_adapter()
    team_adapter = get_team_adapter()

    request = JoinOpenChampionshipRequestModel(data)
    interactor = JoinOpenChampionshipInteractor(
        request=request,
        championship_adapter=championship_adapter,
        player_adapter=player_adapter,
        team_adapter=team_adapter)

    try:
        response = interactor.run()
    except JoinOpenChampionshipException as exc:
        return server_error(str(exc))

    return success(response)


@bp_add_friend_to_championship.route('/', **private_post())
def post_add_friend_to_championship():
    data = bp_add_friend_to_championship.current_request.json_body
    player_id = get_user_id_from_jwt(bp_add_friend_to_championship)
    data.update({'entity_id': player_id})

    championship_adapter = get_championship_adapter()
    player_adapter = get_player_adapter()
    team_adapter = get_team_adapter()

    request = AddFriendToChampionshipRequestModel(data)
    interactor = AddFriendToChampionshipInteractor(
        request=request,
        championship_adapter=championship_adapter,
        player_adapter=player_adapter,
        team_adapter=team_adapter)

    try:
        response = interactor.run()
    except AddFriendToChampionshipException as exc:
        return server_error(str(exc))

    return success(response)
