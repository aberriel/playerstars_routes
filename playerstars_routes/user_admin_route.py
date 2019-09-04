from chalice import Blueprint
from playerstars_adapters import UserAdminAdapter
from playerstars_domain import UserAdmin
from playerstars_routes.chalice_support import (
    private_get, private_put, private_post)

from .basic_entity_route import BasicEntityRoute
from playerstars_routes.settings import Settings

bp_user_admin = Blueprint(__name__)


def get_router():
    adapter = UserAdminAdapter(Settings.USER_ADMIN_TABLE_NAME)
    return BasicEntityRoute(adapter, UserAdmin, 'user-admin')


@bp_user_admin.route('/', **private_get())
def get_all_user_admin():
    return get_router().get_all()


@bp_user_admin.route('/{entity_id}', **private_get())
def get_user_admin_by_id(region_id):
    return get_router().get_by_id(region_id)


@bp_user_admin.route('/', **private_post())
def post_user_admin():
    data = bp_user_admin.current_request.json_body
    return get_router().post(data)


@bp_user_admin.route('/{entity_id}', **private_put())
def put_user_admin(entity_id):
    data = bp_user_admin.current_request.json_body
    return get_router().put(data)
