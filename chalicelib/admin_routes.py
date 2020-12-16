from uuid import uuid4

from chalice import Blueprint
from chalice_support import server_error, success, unauthorized
from playerstars_adapters import (
    ConsoleAdapter,
    DuelAdapter,
    PlayerAdapter,
    PrivacyPolicyAdapter,
    TermsAdapter)
from playerstars_domain import Console, Duel, Player, PrivacyPolicy, Terms
from playerstars_interactors import (
    BasicPutRequestModel,
    GetAllGamesAdminException,
    GetAllGamesAdminInteractor,
    PutPlayerIsAdminInteractor,
    UpdateEntityException, GetUploadImageUrlInteractor)

from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.chalice_support import (
    private_delete,
    private_get,
    private_post,
    private_put)
from chalicelib.settings import Settings
from chalicelib.utils import (
    check_admin_authorization,
    get_user_id_from_jwt,
    make_fields_dot,
    UserNotAdminAuthorized)

bp_admin = Blueprint(__name__)


def console_adapter():
    return ConsoleAdapter(Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


def player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def duel_router():
    adapter = DuelAdapter(
        Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Duel, 'duel')


def player_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


def console_router():
    return BasicEntityRoute(console_adapter(), Console, 'console')


def authorize(blueprint):
    user_id = get_user_id_from_jwt(blueprint)
    try:
        check_admin_authorization(user_id)
        return True, None
    except UserNotAdminAuthorized as e:
        return False, e


def get_all_admin(router):
    auth, msg = authorize(bp_admin)
    if not auth:
        return unauthorized(str(msg))

    query_params = make_fields_dot(bp_admin.current_request.query_params)
    return router.get_all(query_params=query_params)


def get_by_id_admin(entity_id, router):
    auth, msg = authorize(bp_admin)
    if auth:
        return router.get_by_id(entity_id)
    return unauthorized(str(msg))


def post_admin(router):
    auth, msg = authorize(bp_admin)
    if auth:
        data = bp_admin.current_request.json_body
        return router.post(data)
    return unauthorized(str(msg))


def put_admin(router):
    auth, msg = authorize(bp_admin)
    if auth:
        data = bp_admin.current_request.json_body
        return router.put(data)
    return unauthorized(str(msg))


def delete_admin(entity_id, router):
    auth, msg = authorize(bp_admin)
    if auth:
        return router.delete(entity_id)
    return unauthorized(str(msg))


@bp_admin.route('/player', **private_get())
def get_all_players_admin():
    return get_all_admin(player_router())


@bp_admin.route('/player/{entity_id}', **private_get())
def get_player_by_id_admin(entity_id):
    return get_by_id_admin(entity_id, player_router())


@bp_admin.route('/console', **private_get())
def get_all_consoles_admin():
    return get_all_admin(console_router())


@bp_admin.route('/console/{entity_id}', **private_get())
def get_console_by_id_admin(entity_id):
    return get_by_id_admin(entity_id, console_router())


@bp_admin.route('/console', **private_post())
def post_console_admin():
    return post_admin(console_router())


@bp_admin.route('/console/{entity_id}', **private_put())
def put_console_admin(entity_id):
    return put_admin(console_router())


@bp_admin.route('/console/{entity_id}', **private_delete())
def delete_console_admin(entity_id):
    return delete_admin(entity_id, console_router())


@bp_admin.route('/player/{entity_id}', **private_put())
def put_player_admin(entity_id):
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
        json_data = bp_admin.current_request.json_body
        request = BasicPutRequestModel(json_data)
        interactor = PutPlayerIsAdminInteractor(
            request, player_adapter(), Player)
        response = interactor.run()
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)


@bp_admin.route('/games', **private_get())
def get_all_games_admin():
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
        interactor = GetAllGamesAdminInteractor(
            console_adapter=console_adapter())
        response = interactor.run()()
    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    except GetAllGamesAdminException as e:
        return server_error(str(e))
    return success(response)


@bp_admin.route('/games/upload-mask', **private_get())
def get_upload_mask_url():
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
        object_name = str(uuid4())
        interactor = GetUploadImageUrlInteractor(
            bucket_name=Settings.S3_BUCKET_IMAGE_NAME,
            temp_url_expiration=Settings.S3_TEMP_URL_EXPIRATION,
            folder=Settings.S3_FOLDER_MASK,
            object_name=object_name)

        response = interactor.run()

    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    except BaseException as e:
        return server_error(str(e))
    return success(response)


@bp_admin.route('/games/upload-image', **private_get())
def get_upload_game_url():
    user_id = get_user_id_from_jwt(bp_admin)
    try:
        check_admin_authorization(user_id)
        object_name = str(uuid4())
        interactor = GetUploadImageUrlInteractor(
            bucket_name=Settings.S3_BUCKET_IMAGE_NAME,
            temp_url_expiration=Settings.S3_TEMP_URL_EXPIRATION,
            folder=Settings.S3_FOLDER_GAME,
            object_name=object_name)

        response = interactor.run()

    except UserNotAdminAuthorized as e:
        return unauthorized(str(e))
    except BaseException as e:
        return server_error(str(e))
    return success(response)


@bp_admin.route('/duel', **private_get())
def get_all_duel_admin():
    return get_all_admin(duel_router())


@bp_admin.route('/duel/{entity_id}', **private_get())
def get_duel_by_id_admin(entity_id):
    return get_by_id_admin(entity_id, duel_router())


##################
def terms_router():
    adapter = TermsAdapter(Settings.TERMS_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Terms, 'terms')


@bp_admin.route('/term', **private_get())
def get_all_terms_admin():
    return get_all_admin(terms_router())


@bp_admin.route('/term/{entity_id}', **private_get())
def get_terms_by_id_admin(entity_id):
    return get_by_id_admin(entity_id, terms_router())


@bp_admin.route('/term', **private_post())
def post_terms_admin():
    return post_admin(terms_router())


@bp_admin.route('/term/{entity_id}', **private_put())
def put_terms_admin(entity_id):
    return put_admin(terms_router())


@bp_admin.route('/term/{entity_id}', **private_delete())
def delete_terms_admin(entity_id):
    return delete_admin(entity_id, terms_router())


def privacy_router():
    adapter = PrivacyPolicyAdapter(
        Settings.PRIVACY_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, PrivacyPolicy, 'privacy-policy')


@bp_admin.route('/privacy', **private_get())
def get_all_privacy_admin():
    return get_all_admin(privacy_router())


@bp_admin.route('/privacy/{entity_id}', **private_get())
def get_privacy_by_id_admin(entity_id):
    return get_by_id_admin(entity_id, privacy_router())


@bp_admin.route('/privacy', **private_post())
def post_privacy_admin():
    return post_admin(privacy_router())


@bp_admin.route('/privacy/{entity_id}', **private_put())
def put_privacy_admin(entity_id):
    return put_admin(privacy_router())


@bp_admin.route('/privacy/{entity_id}', **private_delete())
def delete_privacy_admin(entity_id):
    return delete_admin(entity_id, privacy_router())
