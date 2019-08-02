from playerstars_interactors import (
    GetAllStateRegionsInteractor)
from playerstars_routes.chalice_support import (
    success, not_found)
from chalice import Blueprint
from .auth import cors, cupauth

root = Blueprint(__name__)


@root.route('/region-state/',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_all_region_state():
    interactor = GetAllStateRegionsInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhuma região encontrada")









