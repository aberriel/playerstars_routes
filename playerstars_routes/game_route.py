from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import (
    GetAllGamesInteractor, PostGameRequestModel, PostGameInteractor,
    SaveGameException, GetGameInteractor, GetGameRequestModel)
from playerstars_routes.basic_route import BasicRoute


bp_game = Blueprint(__name__)


@bp_game.route('/game/', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_games():
    return GameRoute().get_all()

@bp_game.route(
    '/game/{entity_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_game_by_id(entity_id):
    return GameRoute().get_by_id(entity_id)


@bp_game.route('/game/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_game():
    from app import app
    data = app.current_request.json_body
    return GameRoute().post(data)


class GameRoute(BasicRoute):

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

    def make_put_request(self):
        raise NotImplementedError("Não implementado no interactor")

    def update_exception(self):
        raise NotImplementedError("Não implementado no interactor")

    def put_interactor(self):
        raise NotImplementedError("Não implementado no interactor")

    def delete_request_model(self):
        raise NotImplementedError("Não implementado no interactor")

    def delete_interactor(self):
        raise NotImplementedError("Não implementado no interactor")

    def delete_not_found(self):
        raise NotImplementedError("Não implementado no interactor")
