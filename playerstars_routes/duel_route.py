from chalice import Blueprint

from playerstars_adapters import DuelAdapter, PlayerAdapter
from .basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings
from playerstars_domain import Player, Duel
from playerstars_routes.chalice_support import private_get, private_post

bp_match_list = Blueprint(__name__)
bp_create_duel = Blueprint(__name__)
bp_enter_duel = Blueprint(__name__)


def get_router_match_list():
    adapter = PlayerAdapter(Settings.CONSOLE_TABLE_NAME)
    return BasicEntityRoute(adapter, Player, 'player')


@bp_match_list.route('/{user_id}', **private_get())
def get_match_list(user_id):
    return get_router_match_list().get_by_id(user_id)


def get_router_duel():
    adapter = DuelAdapter(Settings.CONSOLE_TABLE_NAME)
    return BasicEntityRoute(adapter, Duel, 'duel')


@bp_create_duel.route('/', **private_post())
def post_duel():
    data = bp_create_duel.current_request.json_body
    return get_router_duel().post(data)


@bp_enter_duel.route('/', **private_post())
def enter_duel():
    data = bp_enter_duel.current_request.json_body
    return get_router_duel().post(data)
