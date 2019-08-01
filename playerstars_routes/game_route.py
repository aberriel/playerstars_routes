from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_routes.chalice_support import (
    success, not_found, server_error)
from playerstars_interactors import (
    GetAllGamesInteractor, PostGameRequestModel, PostGameInteractor,
    SaveGameException)
from playerstars_domain import Console


root = Blueprint(__name__)


@root.route('/game/',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_all_games():
    interactor = GetAllGamesInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum jogo encontrado")


@root.route('/game/',
            methods=['POST'],
            cors=cors,
            authorizer=cupauth)
def post_game():
    from app import app
    body = app.current_request.json_body
    console_list = list()
    for console in body['consoles']:
        console_list.append(Console(
            name=console['name'],
            entity_id=console['entity_id'],
            logo_path=console['logo_path'],
            tag_name=console['tag_name']
        ))
    request = PostGameRequestModel(
        name=body['name'],
        logo_path=body['logo_path'],
        consoles=console_list
    )
    interactor = PostGameInteractor(request)
    try:
        response = interactor.run()
    except SaveGameException as e:
        return server_error(str(e))
    return success(response)
