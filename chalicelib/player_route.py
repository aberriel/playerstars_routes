from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_domain import Player
from chalicelib.chalice_support import (
    private_get, private_post)

from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

bp_player = Blueprint(__name__)


def get_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


@bp_player.route('/', **private_post())
def post_player():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    print("ENTITY_ID: ", entity_id)
    data.update({'entity_id': entity_id})
    print("DATA: ", data)
    return get_router().post(data)


@bp_player.route('/{entity_id}', **private_get())
def get_player_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_player.route('/', **private_get())
def get_all_player():
    return get_router().get_all()
