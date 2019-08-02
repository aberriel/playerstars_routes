from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import (
    GetAllCountryRegionsInteractor,
    PostRegionCountryRequestModel,
    PostRegionCountryInteractor,
    SaveRegionCountryException)
from playerstars_routes.chalice_support import (
    success, not_found, server_error)

root = Blueprint(__name__)


@root.route('/region-country/',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_all_region_country():
    interactor = GetAllCountryRegionsInteractor
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhuma região encontrada")


@root.route('/region-country/',
            methods=['POST'],
            cors=cors,
            authorizer=cupauth)
def post_region_country():
    from app import app
    body = app.current_request.json_body
    request = PostRegionCountryRequestModel(
        name=body['name'],
        minimum_bet=body['minimum_bet'],
        countries=body['countries']
    )
    interactor = PostRegionCountryInteractor(request)
    try:
        response = interactor.run()
    except SaveRegionCountryException as e:
        return server_error(str(e))
    return success(response)
