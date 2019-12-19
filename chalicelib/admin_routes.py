from chalice import Blueprint
from chalicelib.settings import Settings
from chalicelib.basic_entity_route import BasicEntityRoute
from playerstars_domain import Player
from playerstars_adapters import (
    PlayerAdapter
)
from chalicelib.utils import \
    get_user_id_from_jwt, check_admin_authorization, UserNotAdminAuthorized
from chalicelib.chalice_support import (
    unauthorized
)
from chalicelib.chalice_support import (
    private_get
)

bp_admin = Blueprint(__name__)


def get_player_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


@bp_admin.route('/player', **private_get())
def get_all_players_admin():
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    return get_player_router().get_all()


@bp_admin.route('/player/{entity_id}', **private_get())
def get_player_by_id_admin(entity_id):
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    return get_player_router().get_by_id(entity_id)
