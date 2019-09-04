from chalice import Blueprint
from playerstars_adapters import CountryRegionAdapter
from playerstars_domain import CountryRegion
from playerstars_routes.chalice_support import (
    private_get, private_put, private_post)

from .basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings

bp_region_country = Blueprint(__name__)


def get_router():
    adapter = CountryRegionAdapter(Settings.REGION_COUNTRY_TABLE_NAME)
    return BasicEntityRoute(adapter, CountryRegion, 'region-country')


@bp_region_country.route('/', **private_get())
def get_all_region_country():
    return get_router().get_all()


@bp_region_country.route('/{entity_id}', **private_get())
def get_region_country_by_id(region_id):
    return get_router().get_by_id(region_id)


@bp_region_country.route('/', **private_post())
def post_region_country():
    data = bp_region_country.current_request.json_body
    return get_router().post(data)


@bp_region_country.route('/{entity_id}', **private_put())
def put_region_country(entity_id):
    data = bp_region_country.current_request.json_body
    return get_router().put(data)
