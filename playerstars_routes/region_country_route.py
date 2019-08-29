from chalice import Blueprint
from .auth import cors, cupauth
from playerstars_interactors import (
    GetRegionCountryInteractor, GetAllRegionCountriesInteractor,
    PostRegionCountryRequestModel, PostRegionCountryInteractor,
    GetRegionCountryRequestModel, SaveRegionCountryException,
    PutRegionCountryRequestModel, PutRegionCountryInteractor,
    UpdateRegionCountryException)
from playerstars_routes.basic_route import BasicChaliceRoute

bp_region_country = Blueprint(__name__)


@bp_region_country.route(
    '/region-country/', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_region_country():
    return RegionCountryChaliceRoute().get_all()


@bp_region_country.route(
    '/region-country/{entity_id}', methods=['GET'],
    cors=cors, authorizer=cupauth)
def get_region_country_by_id(region_id):
    return RegionCountryChaliceRoute().get_by_id(region_id)


@bp_region_country.route(
    '/region-country/', methods=['POST'],
    cors=cors, authorizer=cupauth)
def post_region_country():
    from app import app
    data = app.current_request.json_body
    return RegionCountryChaliceRoute().post(data)


@bp_region_country.route(
    '/region-country/{entity_id}', methods=['PUT'],
    cors=cors, authorizer=cupauth)
def put_region_country(entity_id):
    from app import app
    data = app.current_request.json_body
    return RegionCountryChaliceRoute().put(data)


class RegionCountryChaliceRoute(BasicChaliceRoute):

    def make_post_request(self, data):
        return PostRegionCountryRequestModel(
            name=data['name'],
            minimum_bet=data['minimum_bet'],
            countries=data['countries'])

    def make_put_request(self, data):
        return PutRegionCountryRequestModel(
            entity_id=data['entity_id'],
            name=data['name'],
            minimum_bet=data['minimum_bet'],
            countries=data['countries'])

    def get_all_interactor(self):
        return GetAllRegionCountriesInteractor

    def not_found_message(self):
        return 'Região País não encontrada'

    def not_found_all_message(self):
        return 'Nenhuma Região País encontrada'

    def get_request_model(self):
        return GetRegionCountryRequestModel

    def get_interactor(self):
        return GetRegionCountryInteractor

    def save_exception(self):
        return SaveRegionCountryException

    def post_interactor(self):
        return PostRegionCountryInteractor

    def update_exception(self):
        return UpdateRegionCountryException

    def put_interactor(self):
        return PutRegionCountryInteractor

    def delete_request_model(self):
        raise NotImplementedError('Delete não implementado')

    def delete_interactor(self):
        raise NotImplementedError('Delete não implementado')

    def delete_not_found(self):
        raise NotImplementedError('Delete não implementado')
