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
    private_get, private_put)
from chalice_support import unauthorized, server_error, success
from playerstars_interactors import (
    BasicPutRequestModel, PutPlayerIsAdminInteractor, UpdateEntityException
)
bp_admin = Blueprint(__name__)


def get_player_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_admin.route('/player', **private_get())
def get_all_players_admin():
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    query_params = None
    if bp_admin.current_request and bp_admin.current_request.query_params:
        query_params = bp_admin.current_request.query_params
    return get_player_router().get_all(query_params, False)


@bp_admin.route('/player/{entity_id}', **private_get())
def get_player_by_id_admin(entity_id):
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    return get_player_router().get_by_id(entity_id)


@bp_admin.route('/player/{entity_id}', **private_put())
def put_player_admin(entity_id):
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
        json_data = bp_admin.current_request.json_body
        request = BasicPutRequestModel(json_data)
        interactor = PutPlayerIsAdminInteractor(
            request, get_player_adapter(), Player)
        response = interactor.run()
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)
