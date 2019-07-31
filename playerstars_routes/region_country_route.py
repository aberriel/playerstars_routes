from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import GetAllCountryRegionsInteractor
from playerstars_routes.chalice_support import success, not_found

root = Blueprint(__name__)


@root.route('/region-country',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_all_region_country():
    interactor = GetAllCountryRegionsInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhuma região encontrada")
