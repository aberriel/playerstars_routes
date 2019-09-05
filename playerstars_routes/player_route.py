from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_domain import Player
from playerstars_routes.chalice_support import (
    private_get, private_post)

from playerstars_routes.basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings

bp_player = Blueprint(__name__)


def get_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


@bp_player.route('/', **private_post())
def post_player():
    data = bp_player.current_request.json_body
    return get_router().post(data)


@bp_player.route('/{entity_id}', **private_get())
def get_player_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_player.route('/', **private_get())
def get_all_player():
    return get_router().get_all()
