from chalice import Blueprint
from playerstars_adapters import ConvertStarRateAdapter
from playerstars_domain import ConvertStarRate
from chalicelib.chalice_support import private_get, private_delete, private_put, private_post

from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings

bp_convert = Blueprint(__name__)


def get_router():
    adapter = ConvertStarRateAdapter(Settings.CONVERT_STAR_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, ConvertStarRate, 'convert-rate')


@bp_convert.route('/', **private_get())
def get_all_convert_rate():
    return get_router().get_all()


@bp_convert.route('/{entity_id}', **private_get())
def get_convert_rate_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_convert.route('/', **private_post())
def post_convert_rate():
    data = bp_convert.current_request.json_body
    return get_router().post(data)


@bp_convert.route('/{entity_id}', **private_put())
def put_convert_rate(entity_id):
    data = bp_convert.current_request.json_body
    return get_router().put(data)


@bp_convert.route('/{entity_id}', **private_delete())
def delete_convert_rate(entity_id):
    return get_router().delete(entity_id)
