from chalice import Blueprint
from playerstars_adapters import TeamAdapter
from playerstars_domain import Team
from playerstars_interactors import (
    GetTeamByUserInteractor, GetTeamByUserRequestModel, MembershipType)

from playerstars_routes.chalice_support import (
    private_get, private_put, private_post)
from playerstars_routes.basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings
from playerstars_routes.chalice_support import success, not_found

bp_team = Blueprint(__name__)


def get_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


def get_router():
    return BasicEntityRoute(get_adapter(), Team, 'team')


@bp_team.route('/', **private_get())
def get_all_teams():
    return get_router().get_all()


@bp_team.route('/{entity_id}', **private_get())
def get_team_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_team.route('/byuser/{player_id}', **private_get())
def get_all_teams_by_user(player_id):
    return get_by_user(player_id)


@bp_team.route('/', **private_post())
def post_team():
    data = bp_team.current_request.json_body
    return get_router().post(data)


@bp_team.route('/{entity_id}', **private_put())
def put_team(entity_id):
    data = bp_team.current_request.json_body
    return get_router().put(data)


def get_by_user(player_id):
    request = GetTeamByUserRequestModel(membership_type=MembershipType.ALL,
                                        player_id=player_id)
    interactor = GetTeamByUserInteractor(request, get_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found('Não foram encontradas teams para esse player')
