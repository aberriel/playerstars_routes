from chalice import Blueprint
from .auth import cors
from playerstars_interactors import (
    GetAllGamesInteractor, PostGameRequestModel, PostGameInteractor,
    SaveGameException)
from playerstars_routes.basic_route import BasicRoute


bp_game = Blueprint(__name__)


@bp_game.route('/game/', methods=['GET'], cors=cors)
def get_all_games():
    return GameRoute().get_all()


@bp_game.route('/game/', methods=['POST'], cors=cors)
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
        raise NotImplementedError("Não implementado no interactor")

    def not_found_all_message(self):
        return "Nenhum jogo encontrado"

    def get_request_model(self):
        raise NotImplementedError("Não implementado no interactor")

    def get_interactor(self):
        raise NotImplementedError("Não implementado no interactor")

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

