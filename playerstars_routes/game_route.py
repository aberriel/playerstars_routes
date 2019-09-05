from chalice import Blueprint
from playerstars_adapters import ConsoleAdapter
from playerstars_domain import Console
from playerstars_routes.chalice_support import (
    private_get, private_put, private_post, private_delete)

from playerstars_routes.basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings

bp_game = Blueprint(__name__)


def get_router():
    adapter = ConsoleAdapter(
        Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Console, 'game')


@bp_game.route('/', **private_get())
def get_all_games():
    return get_router().get_all()


@bp_game.route('/{entity_id}', **private_get())
def get_game_by_id(region_id):
    return get_router().get_by_id(region_id)


@bp_game.route('/', **private_post())
def post_game():
    data = bp_game.current_request.json_body
    return get_router().post(data)


@bp_game.route('/{entity_id}', **private_put())
def put_game(entity_id):
    data = bp_game.current_request.json_body
    return get_router().put(data)


@bp_game.route('/{entity_id}', **private_delete())
def delete_game(entity_id):
    return get_router().delete(entity_id)
