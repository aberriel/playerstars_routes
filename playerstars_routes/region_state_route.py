from chalice import Blueprint
from playerstars_adapters import StateRegionAdapter
from playerstars_domain import StateRegion
from playerstars_routes.chalice_support import (
    private_get, private_put, private_post)

from .basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings

bp_region_state = Blueprint(__name__)


def get_router():
    adapter = StateRegionAdapter(Settings.REGION_STATE_TABLE_NAME)
    return BasicEntityRoute(adapter, StateRegion, 'region-state')


@bp_region_state.route('/', **private_get())
def get_all_region_state():
    return get_router().get_all()


@bp_region_state.route('/{entity_id}', **private_get())
def get_region_state_by_id(region_id):
    return get_router().get_by_id(region_id)


@bp_region_state.route('/', **private_post())
def post_region_state():
    data = bp_region_state.current_request.json_body
    return get_router().post(data)


@bp_region_state.route('/{entity_id}', **private_put())
def put_region_state(entity_id):
    data = bp_region_state.current_request.json_body
    return get_router().put(data)
