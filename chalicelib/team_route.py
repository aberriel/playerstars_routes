from chalice import Blueprint
from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.chalice_support import (
    private_delete,
    private_get,
    private_put,
    private_post)
from chalicelib.settings import Settings
from chalice_support import success, not_found, created, server_error
from chalicelib.utils import get_user_id_from_jwt
from playerstars_adapters import (
    PlayerAdapter,
    TeamAdapter
)
from playerstars_domain import Team
from playerstars_interactors import (
    AcceptTeamInvitationException,
    AcceptTeamInvitationInteractor,
    AcceptTeamInvitationRequestModel,
    DeleteTeamException,
    DeleteTeamInteractor,
    DeleteTeamRequestModel,
    EnterTeamException,
    EnterTeamInteractor,
    EnterTeamRequestModel,
    GetTeamByUserInteractor,
    GetTeamByUserRequestModel,
    LeaveTeamException,
    LeaveTeamInteractor,
    LeaveTeamRequestModel,
    PostTeamInteractor,
    PostTeamRequestModel,
    PutTeamInteractor,
    PutTeamRequestModel,
    SaveTeamException,
    UpdateEntityException)


bp_enter_team = Blueprint(__name__)
bp_leave_team = Blueprint(__name__)
bp_team = Blueprint(__name__)


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def get_router():
    return BasicEntityRoute(get_team_adapter(), Team, 'team')


@bp_team.route('/', **private_get())
def get_all_teams():
    return get_router().get_all()


@bp_team.route('/{entity_id}', **private_get())
def get_team_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_team.route('/byuser/{player_id}', **private_get())
def get_all_teams_by_user(player_id):
    return get_by_user(player_id)


def get_by_user(player_id):
    request = GetTeamByUserRequestModel(player_id=player_id)
    interactor = GetTeamByUserInteractor(request, get_team_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found('No teams found for this player')


@bp_team.route('/', **private_post())
def post_team():
    data = bp_team.current_request.json_body
    player_id = get_user_id_from_jwt(bp_team)
    data.update({'captain_id': player_id})
    return post(data)


def post(data):
    request = PostTeamRequestModel(data)
    interactor = PostTeamInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter(),
        settings=Settings)
    try:
        response = interactor.run()
    except SaveTeamException as e:
        return server_error(str(e))
    return created(response)


@bp_team.route('/{entity_id}', **private_put())
def put_team(entity_id):
    data = bp_team.current_request.json_body
    return put(data)


def put(data):
    request = PutTeamRequestModel(**data)
    interactor = PutTeamInteractor(
        request, get_player_adapter(), get_team_adapter(), Settings)
    try:
        response = interactor.run()
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)


@bp_team.route('/enter', **private_post())
def enter_team():
    data = bp_team.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_team)
    data.update({'player_id': entity_id})
    return enter_team_post(data)


def enter_team_post(json_data):
    request = EnterTeamRequestModel(json_data)
    interactor = EnterTeamInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter()
    )
    try:
        response = interactor.run()
    except EnterTeamException as e:
        return server_error(str(e))
    return success(response)


@bp_leave_team.route('/', **private_put())
def leave_team():
    data = bp_leave_team.current_request.json_body
    player_id = get_user_id_from_jwt(bp_leave_team)
    data.update({'player_id': player_id})
    return leave_team_post(data)


def leave_team_post(json_data):
    request = LeaveTeamRequestModel(json_data)
    interactor = LeaveTeamInteractor(
        request=request,
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except LeaveTeamException as e:
        return server_error(str(e))
    return success(response)


@bp_team.route('/', **private_delete())
def delete_team():
    data = bp_team.current_request.json_body
    player_id = get_user_id_from_jwt(bp_team)
    data.update({'player_id': player_id})
    return delete_team_post(data)


def delete_team_post(json_data):
    request = DeleteTeamRequestModel(json_data)
    interactor = DeleteTeamInteractor(
        request=request,
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except DeleteTeamException as e:
        return server_error(str(e))
    return success(response)


@bp_team.route('/accept-invitation', **private_post())
def accept_invitation():
    data = bp_team.current_request.json_body
    player_id = get_user_id_from_jwt(bp_team)
    data.update({'player_id': player_id})
    return accept_invitation_post(data)


def accept_invitation_post(json_data):
    request = AcceptTeamInvitationRequestModel(json_data)
    interactor = AcceptTeamInvitationInteractor(
        request=request,
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except AcceptTeamInvitationException as e:
        return server_error(str(e))
    return success(response)
