from playerstars_interactors import (
    GetAllStateRegionsInteractor,
    GetRegionStateRequestModel,
    PostRegionStateRequestModel,
    PostRegionStateInteractor,
    GetRegionStateInteractor,
    GetRegionStateResponseModel,
    SaveRegionStateException)
from playerstars_routes.chalice_support import (
    success, not_found, server_error)
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


@root.route('/region-state/{region_id}',
            methods=['GET'],
            cors=cors,
            authorizer=cupauth)
def get_region_state(region_id):
    request = GetRegionStateRequestModel(region_id)
    interactor = GetRegionStateInteractor(request)
    response: GetRegionStateResponseModel = interactor.run()
    if not response:
        return not_found("Região não encontrada")
    return success(response)


@root.route('/region-state/',
            methods=['POST'],
            cors=cors,
            authorizer=cupauth)
def post_region_state():
    from app import app
    body = app.current_request.json_body
    request = PostRegionStateRequestModel(
        name=body['name'],
        minimum_bet=body['minimum_bet'],
        states=body['states']
    )
    interactor = PostRegionStateInteractor(request)
    try:
        response = interactor.run()
    except SaveRegionStateException as e:
        return server_error(str(e))
    return success(response)
