from chalice import Blueprint
from playerstars_adapters import ValuesAdapter
from playerstars_domain import Values
from chalicelib.chalice_support import (
    private_get, private_delete, private_put, private_post)

from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings

bp_value = Blueprint(__name__)


def get_router():
    adapter = ValuesAdapter(
        Settings.VALUES_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Values, 'convert-rate')


@bp_value.route('/', **private_get())
def get_all_values():
    return get_router().get_all()


@bp_value.route('/{entity_id}', **private_get())
def get_value_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_value.route('/', **private_post())
def post_value():
    data = bp_value.current_request.json_body
    return get_router().post(data)


@bp_value.route('/{entity_id}', **private_put())
def put_value(entity_id):
    data = bp_value.current_request.json_body
    return get_router().put(data)


@bp_value.route('/{entity_id}', **private_delete())
def delete_value(entity_id):
    return get_router().delete(entity_id)
