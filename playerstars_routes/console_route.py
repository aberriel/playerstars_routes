from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_routes.chalice_support import (
    success, not_found, server_error, bad_request, created)
from playerstars_interactors import (
    GetAllConsolesInteractor, PostConsoleRequestModel, PostConsoleInteractor,
    SaveConsoleException, GetConsoleInteractor, GetConsoleRequestModel,
    GetConsoleResponseModel)

root = Blueprint(__name__)


@root.route('/console/',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_all_consoles():
    interactor = GetAllConsolesInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum console encontrado")


@root.route('/console/{console_id}',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_console(console_id):
    request = GetConsoleRequestModel(console_id)
    interactor = GetConsoleInteractor(request)
    response: GetConsoleResponseModel = interactor.run()
    if not response:
        return not_found("Console não encontrado")
    return success(response)


@root.route('/console/',
            methods=['POST'],
            cors=cors,
            authorizer=cupauth)
def post_console():
    from app import app
    data = app.current_request.json_body
    request = PostConsoleRequestModel(
        name=data['name'],
        logo_path=data['logo_path'],
        games=data['games'],
        tag_name=data['tag_name'])
    interactor = PostConsoleInteractor(request)
    try:
        response = interactor.run()
    except SaveConsoleException as e:
        return server_error(str(e))
    return created(response)
