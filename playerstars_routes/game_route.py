from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import GetAllGamesInteractor
from playerstars_routes.chalice_support import success, not_found

root = Blueprint(__name__)


@root.route('/game',
            methods=['GET', 'POST'],
            cors=cors,
            authorizer=cupauth)
def get_all_games():
    interactor = GetAllGamesInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum jogo encontrado")
