from chalice import Blueprint
from playerstars_interactors import (
    GetAllConsolesInteractor, PostConsoleRequestModel, PostConsoleInteractor,
    SaveConsoleException, GetConsoleInteractor, GetConsoleRequestModel,
    GetConsoleResponseModel, PutConsoleInteractor,
    PutConsoleRequestModel, UpdateConsoleException, DeleteConsoleInteractor,
    DeleteConsoleRequestModel)
from playerstars_routes.basic_route import BasicRoute

root = Blueprint(__name__)


class ConsoleRoute(BasicRoute):
    def make_post_request(self, data):
        return PostConsoleRequestModel(
            name=data['name'],
            logo_path=data['logo_path'],
            games=data['games'],
            tag_name=data['tag_name'])

    def make_put_request(self, data):
        return PutConsoleRequestModel(
            console_id=data['entity_id'],
            name=data['name'],
            logo_path=data['logo_path'],
            games=data['games'],
            tag_name=data['tag_name']
        )

    def get_all_interactor(self):
        return GetAllConsolesInteractor

    def not_found_message(self):
        return 'Console não encontrado'

    def not_found_all_message(self):
        return 'Nenhum console encontrado'

    def get_request_model(self):
        return GetConsoleRequestModel

    def get_interactor(self):
        return GetConsoleInteractor

    def save_exception(self):
        return SaveConsoleException

    def post_interactor(self):
        return PostConsoleInteractor

    def update_exception(self):
        return UpdateConsoleException

    def put_interactor(self):
        return PutConsoleInteractor

    def delete_request_model(self):
        return DeleteConsoleRequestModel

    def delete_interactor(self):
        return DeleteConsoleInteractor

    def delete_not_found(self):
        return 'Console não encontrado para ser deletado'
