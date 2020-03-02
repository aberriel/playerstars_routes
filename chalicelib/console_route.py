from chalice import Blueprint
from playerstars_adapters import (
    ConsoleAdapter,
    PlayerAdapter)
from playerstars_domain import Console
from playerstars_interactors import (
    AccessDeniedAdminException,
    GetConsoleByIdAdminException,
    GetConsoleByIdAdminInteractor,
    GetConsoleByIdAdminRequestModel,
    GetConsolesAdminException,
    GetConsolesAdminInteractor,
    GetConsolesAdminRequestModel,
    PutConsoleAdminException,
    PutConsoleAdminInteractor,
    PutConsoleAdminRequestModel)
from chalicelib.chalice_support import (
    private_get,
    private_delete,
    private_put,
    private_post)
from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from chalice_support import (
    not_found,
    server_error,
    success,
    unauthorized
)


bp_console = Blueprint(__name__)
bp_console_admin = Blueprint(__name__)


def get_console_adapter():
    return ConsoleAdapter(Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def get_router():
    adapter = get_console_adapter()
    return BasicEntityRoute(adapter, Console, 'console')


@bp_console.route('/', **private_get())
def get_all_console():
    return get_router().get_all()


@bp_console_admin.route('/', **private_get())
def get_all_consoles_admin():
    player_id = get_user_id_from_jwt(bp_console_admin)
    request = GetConsolesAdminRequestModel(player_id)
    interactor = GetConsolesAdminInteractor(
        request=request,
        console_adapter=get_console_adapter(),
        player_adapter=get_player_adapter())
    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found('No console found')
    except GetConsolesAdminException as e:
        return server_error(str(e))
    except AccessDeniedAdminException as ade:
        return unauthorized(str(ade))


@bp_console_admin.route('/get-console', **private_get())
def get_console_by_id_admin():
    player_id = get_user_id_from_jwt(bp_console_admin)
    data = bp_console_admin.current_request.json_body
    data.update({'player_id': player_id})
    request = GetConsoleByIdAdminRequestModel(data)
    interactor = GetConsoleByIdAdminInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        console_adapter=get_console_adapter())

    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found('Console not found')
    except GetConsoleByIdAdminException as e:
        return server_error(str(e))
    except AccessDeniedAdminException as ade:
        return unauthorized(str(ade))


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


@bp_console_admin.route('/{entity_id}', **private_put())
def put_console_admin(entity_id):
    player_id = get_user_id_from_jwt(bp_console_admin)
    data = bp_console_admin.current_request.json_body
    data.update({'player_id': player_id})
    request = PutConsoleAdminRequestModel(data)
    interactor = PutConsoleAdminInteractor(
        request=request,
        console_adapter=get_console_adapter(),
        player_adapter=get_player_adapter(),
        s3_bucket_name=Settings.S3_BUCKET_NAME,
        s3_bucket_url=Settings.S3_BUCKET_URL)

    try:
        response = interactor.run()
        return success(response)
    except PutConsoleAdminException as pae:
        return server_error(str(pae))
    except AccessDeniedAdminException as ade:
        return unauthorized(str(ade))


@bp_console.route('/{entity_id}', **private_delete())
def delete_console(entity_id):
    return get_router().delete(entity_id)
