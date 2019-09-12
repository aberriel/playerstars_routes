# from chalice import Blueprint
from playerstars_adapters import ConsoleAdapter
from playerstars_domain import Console
from chalicelib.chalice_support import (
    private_get, private_put, private_post, private_delete)
#
# from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
#
# bp_game = Blueprint(__name__)
#
#
# def get_router():
#     adapter = ConsoleAdapter(
#         Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)
#     return BasicEntityRoute(adapter, Console, 'game')
#
#
# @bp_game.route('/', **private_get())
# def get_all_games():
#     return get_router().get_all()
#
#
# @bp_game.route('/{entity_id}', **private_get())
# def get_game_by_id(region_id):
#     return get_router().get_by_id(region_id)
#
#
# @bp_game.route('/', **private_post())
# def post_game():
#     data = bp_game.current_request.json_body
#     return get_router().post(data)
#
#
# @bp_game.route('/{entity_id}', **private_put())
# def put_game(entity_id):
#     data = bp_game.current_request.json_body
#     return get_router().put(data)
#
#
# @bp_game.route('/{entity_id}', **private_delete())
# def delete_game(entity_id):
#     return get_router().delete(entity_id)

from chalice import Blueprint
from chalicelib.chalice_support.auth import cors, cupauth
from playerstars_interactors import (
    BasicPostInteractor, SaveEntityException, PostGameRequestModel,
    GetAllGamesInteractor, PostGameRequestModel, PostGameInteractor,
    SaveGameException, GetGameInteractor, GetGameRequestModel,
    GetAllGamesRequestModel, PutGameRequestModel,
    PutGameInteractor, DeleteGameInteractor,
    DeleteGameRequestModel, UpdateGameException)
from chalicelib.chalice_support import (
        success, not_found,
        created, server_error)

bp_game = Blueprint(__name__)


def get_adapter():
    return ConsoleAdapter(
        Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_game.route(
    '/game/{console_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_games(console_id):
    pass
    # return GameChaliceRoute().get_all_by_console_id(console_id)


@bp_game.route(
    '/game/{entity_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_game_by_id(entity_id):
    pass
    # return GameChaliceRoute().get_by_id(entity_id)


@bp_game.route('/', **private_post())
def post_game():
    data = bp_game.current_request.json_body
    return post(data)


def post(json_data):
    request = PostGameRequestModel(json_data)
    interactor = PostGameInteractor(request, get_adapter(), Console)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


@bp_game.route(
    '/game/{entity_id}', methods=['PUT'], cors=cors, authorizer=cupauth)
def put_game(entity_id):
    from app import app
    data = app.current_request.json_body
    pass
    # return GameChaliceRoute().put(data)


@bp_game.route(
    '/{entity_id}', methods=['DELETE'], cors=cors, authorizer=cupauth)
def delete_game(entity_id):
    print(" A D A P T E R ------>", get_adapter().list_all())
    return delete(entity_id)


def delete(entity_id):
    request = DeleteGameRequestModel(entity_id)
    interactor = DeleteGameInteractor(request, get_adapter())
    response = interactor.run()
    if not response:
        return not_found('Game não encontrado')
    return success(response)


#
# class GameChaliceRoute(BasicChaliceRoute):
#
#     def get_all_by_console_id(self, entity_id):
#         request = GetAllGamesRequestModel(entity_id)
#         response = GetAllGamesInteractor(request).run()
#         if response:
#             return success(response)
#         return not_found(self.not_found_all_message())
#
#     def make_post_request(self, data):
#         return PostGameRequestModel(
#             name=data['name'],
#             logo_path=data['logo_path'],
#             consoles=data['consoles'])
#
#     def get_all_interactor(self):
#         return GetAllGamesInteractor
#
#     def not_found_message(self):
#         return "Jogo não encontrado"
#
#     def not_found_all_message(self):
#         return "Nenhum jogo encontrado"
#
#     def get_request_model(self):
#         return GetGameRequestModel
#
#     def get_interactor(self):
#         return GetGameInteractor
#
#     def save_exception(self):
#         return SaveGameException
#
#     def post_interactor(self):
#         return PostGameInteractor
#
#     def make_put_request(self, data):
#         return PutGameRequestModel(
#             entity_id=data['entity_id'],
#             name=data['name'],
#             logo_path=data['logo_path'],
#             consoles=data['consoles']
#         )
#
#     def update_exception(self):
#         return UpdateGameException
#
#     def put_interactor(self):
#         return PutGameInteractor
#
#     def delete_request_model(self):
#         return DeleteGameRequestModel
#
#     def delete_interactor(self):
#         return DeleteGameInteractor
#
#     def delete_not_found(self):
#         return 'Game não encontrado para deletar'
