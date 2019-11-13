from playerstars_adapters import ConsoleAdapter
from playerstars_domain import Console
from chalicelib.chalice_support import (
    private_get, private_put, private_post, private_delete)
from chalicelib.settings import Settings
from chalice import Blueprint
from playerstars_interactors import (
    DeleteGameInteractor,
    DeleteGameRequestModel,
    GetAllGamesInteractor,
    GetAllGamesRequestModel,
    GetGameInteractor,
    GetGameRequestModel,
    PostGameInteractor,
    PostGameRequestModel,
    PutGameInteractor,
    PutGameRequestModel,
    SaveEntityException,
    UpdateEntityException)
from chalicelib.chalice_support import (
    created,
    not_found,
    server_error,
    success)

bp_game = Blueprint(__name__)
bp_game_by_console = Blueprint(__name__)


def get_adapter():
    return ConsoleAdapter(
        Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_game_by_console.route(
    '/{entity_id}', **private_get())
def get_all_games(entity_id):
    return get_all_by_console_id(entity_id)


@bp_game.route(
    '/{entity_id}', **private_get())
def get_game_by_id(entity_id):
    return get(entity_id)


@bp_game.route('/', **private_post())
def post_game():
    data = bp_game.current_request.json_body
    return post(data)


@bp_game.route(
    '/{entity_id}', **private_put())
def put_game(entity_id):
    data = bp_game.current_request.json_body
    return put(data)


@bp_game.route(
    '/{entity_id}', **private_delete())
def delete_game(entity_id):
    return delete(entity_id)


def get_all_by_console_id(entity_id):
    request = GetAllGamesRequestModel(entity_id)
    interactor = GetAllGamesInteractor(request, get_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found('No jogo found')


def get(game_id):
    request = GetGameRequestModel(game_id)
    interactor = GetGameInteractor(request, get_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Game not found")


def post(json_data):
    request = PostGameRequestModel(json_data)
    interactor = PostGameInteractor(request, get_adapter(), Console)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


def put(json_data):
    request = PutGameRequestModel(json_data)
    interactor = PutGameInteractor(request, get_adapter(), Console)
    try:
        response = interactor.run()
    except UpdateEntityException as ex:
        return server_error(str(ex))
    return success(response)


def delete(entity_id):
    request = DeleteGameRequestModel(entity_id)
    interactor = DeleteGameInteractor(request, get_adapter())
    response = interactor.run()
    if not response:
        return not_found('Game not found')
    return success(response)
