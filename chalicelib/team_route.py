from chalice import Blueprint
from playerstars_adapters import TeamAdapter, PlayerAdapter
from playerstars_domain import Team
from playerstars_interactors import (
    GetTeamByUserInteractor, GetTeamByUserRequestModel,
    PostTeamRequestModel, PostTeamInteractor, SaveEntityException,
    PutTeamInteractor, PutTeamRequestModel, UpdateEntityException,
    EnterTeamRequestModel, EnterTeamInteractor, EnterTeamException)

from chalicelib.chalice_support import (
    private_get, private_put, private_post)
from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
from chalicelib.chalice_support import \
    success, not_found, created, server_error

bp_team = Blueprint(__name__)
bp_enter_team = Blueprint(__name__)


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
    return post(data)


def post(data):
    request = PostTeamRequestModel(**data)
    interactor = PostTeamInteractor(
        request, get_player_adapter(), get_team_adapter(), Settings)
    try:
        response = interactor.run()
    except SaveEntityException as e:
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


@bp_enter_team.route('/', **private_post())
def enter_team():
    data = bp_enter_team.current_request.json_body
    return enter_team_post(data)


def enter_team_post(json_data):
    request = EnterTeamRequestModel(json_data)
    interactor = EnterTeamInteractor(
        request=request, player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter()
    )
    try:
        response = interactor.run()
    except EnterTeamException as e:
        return server_error(str(e))
    return success(response)
