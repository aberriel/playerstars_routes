from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import (
    GetAllRegionStatesInteractor, GetRegionStateRequestModel,
    PostRegionStateRequestModel, PostRegionStateInteractor,
    GetRegionStateInteractor, SaveRegionStateException,
    PutRegionStateInteractor, UpdateRegionStateException,
    PutRegionStateRequestModel)
from playerstars_routes.basic_route import BasicRoute

bp_region_state = Blueprint(__name__)


@bp_region_state.route(
    '/region-state/', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_region_state():
    return RegionStateRoute().get_all()


@bp_region_state.route(
    '/region-state/{entity_id}', methods=['GET'],
    cors=cors, authorizer=cupauth)
def get_region_state_by_id(region_id):
    return RegionStateRoute().get_by_id(region_id)


@bp_region_state.route(
    '/region-state/', methods=['POST'],
    cors=cors, authorizer=cupauth)
def post_region_state():
    from app import app
    data = app.current_request.json_body
    return RegionStateRoute().post(data)


@bp_region_state.route(
    '/region-state/', methods=['PUT'],
    cors=cors, authorizer=cupauth)
def put_region_state():
    from app import app
    data = app.current_request.json_body
    return RegionStateRoute().put(data)


class RegionStateRoute(BasicRoute):

    def make_post_request(self, data):
        return PostRegionStateRequestModel(
            name=data['name'],
            minimum_bet=data['minimum_bet'],
            states=data['states'])

    def make_put_request(self, data):
        return PutRegionStateRequestModel(
            entity_id=data['entity_id'],
            name=data['name'],
            minimum_bet=data['minimum_bet'],
            states=data['states']
        )

    def get_all_interactor(self):
        return GetAllRegionStatesInteractor

    def not_found_message(self):
        return 'Região Estado não encontrada'

    def not_found_all_message(self):
        return 'Nenhuma Região Estado encontrada'

    def get_request_model(self):
        return GetRegionStateRequestModel

    def get_interactor(self):
        return GetRegionStateInteractor

    def save_exception(self):
        return SaveRegionStateException

    def post_interactor(self):
        return PostRegionStateInteractor

    def update_exception(self):
        return UpdateRegionStateException

    def put_interactor(self):
        return PutRegionStateInteractor

    def delete_request_model(self):
        raise NotImplementedError('Delete não implementado')

    def delete_interactor(self):
        raise NotImplementedError('Delete não implementado')

    def delete_not_found(self):
        raise NotImplementedError('Delete não implementado')
