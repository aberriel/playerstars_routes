from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import (
    GetAllGamesInteractor, PostGameRequestModel, PostGameInteractor,
    SaveGameException, GetGameInteractor, GetGameRequestModel,
    GetAllGamesRequestModel, PutGameRequestModel,
    PutGameInteractor, DeleteGameInteractor,
    DeleteGameRequestModel, UpdateGameException)
from playerstars_routes.basic_chalice_route import BasicChaliceRoute
from playerstars_routes.chalice_support import success, not_found

bp_game = Blueprint(__name__)


@bp_game.route(
    '/game/{console_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_games(console_id):
    return GameChaliceRoute().get_all_by_console_id(console_id)


@bp_game.route(
    '/game/{entity_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_game_by_id(entity_id):
    return GameChaliceRoute().get_by_id(entity_id)


@bp_game.route('/game/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_game():
    from app import app
    data = app.current_request.json_body
    return GameChaliceRoute().post(data)


@bp_game.route(
    '/game/{entity_id}', methods=['PUT'], cors=cors, authorizer=cupauth)
def put_game(entity_id):
    from app import app
    data = app.current_request.json_body
    return GameChaliceRoute().put(data)


@bp_game.route(
    '/game/{entity_id}', methods=['DELETE'], cors=cors, authorizer=cupauth)
def delete_game(entity_id):
    return GameChaliceRoute().delete(entity_id)


class GameChaliceRoute(BasicChaliceRoute):

    def get_all_by_console_id(self, entity_id):
        request = GetAllGamesRequestModel(entity_id)
        response = GetAllGamesInteractor(request).run()
        if response:
            return success(response)
        return not_found(self.not_found_all_message())

    def make_post_request(self, data):
        return PostGameRequestModel(
            name=data['name'],
            logo_path=data['logo_path'],
            consoles=data['consoles'])

    def get_all_interactor(self):
        return GetAllGamesInteractor

    def not_found_message(self):
        return "Jogo não encontrado"

    def not_found_all_message(self):
        return "Nenhum jogo encontrado"

    def get_request_model(self):
        return GetGameRequestModel

    def get_interactor(self):
        return GetGameInteractor

    def save_exception(self):
        return SaveGameException

    def post_interactor(self):
        return PostGameInteractor

    def make_put_request(self, data):
        return PutGameRequestModel(
            entity_id=data['entity_id'],
            name=data['name'],
            logo_path=data['logo_path'],
            consoles=data['consoles']
        )

    def update_exception(self):
        return UpdateGameException

    def put_interactor(self):
        return PutGameInteractor

    def delete_request_model(self):
        return DeleteGameRequestModel

    def delete_interactor(self):
        return DeleteGameInteractor

    def delete_not_found(self):
        return 'Game não encontrado para deletar'
