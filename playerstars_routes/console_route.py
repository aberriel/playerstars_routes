from chalice import Blueprint
from playerstars_adapters import ConsoleAdapter
from playerstars_domain import Console

from playerstars_routes import BasicEntityRoute
from playerstars_routes.settings import Settings
from .auth import cors, cupauth

bp_console = Blueprint(__name__)


def private(method):
    return dict(methods=[method], cors=cors, authorizer=cupauth)


def private_get():
    return private('GET')


def private_put():
    return private('PUT')


def private_post():
    return private('POST')


def private_delete():
    return private('DELETE')


def get_router():
    adapter = ConsoleAdapter(Settings.CONSOLE_TABLE_NAME)
    return BasicEntityRoute(adapter, Console, 'console')


@bp_console.route('/', **private_get())
def get_all_console():
    return get_router().get_all()


@bp_console.route('/{entity_id}', **private_get())
def get_console_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_console.route('/', **private_post())
def post_console():
    data = bp_console.current_request.json_body
    return get_router().post(data)


@bp_console.route('/{entity_id}', **private_put())
def put_console(entity_id):
    data = bp_console.current_request.json_body
    return get_router().put(data)


@bp_console.route('/{entity_id}', **private_delete())
def delete_console(entity_id):
    return get_router().delete(entity_id)
