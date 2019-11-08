from chalicelib.chalice_support.api_responses import (
    created, not_found, server_error, success)
from playerstars_interactors import BasicGetAllInteractor
from playerstars_interactors import (
    BasicGetRequestModel, BasicGetInteractor)
from playerstars_interactors import (
    BasicPostRequestModel, BasicPostInteractor, SaveEntityException)
from playerstars_interactors import (
    BasicPutRequestModel,  BasicPutInteractor,  UpdateEntityException)
from playerstars_interactors import (
    BasicDeleteInteractor, BasicDeleteRequestModel)


class BasicEntityRoute:
    def __init__(self, adapter_instance, entity_class, entity_name='objeto'):
        self.adapter_instance = adapter_instance
        self.entity_class = entity_class
        self.entity_name = entity_name

    def get_all(self):
        try:
            interactor = BasicGetAllInteractor(self.adapter_instance)
            response = interactor.run()
            if response:
                return success(response)
            return not_found(f'Nenhum {self.entity_name} encontrado')
        except BaseException as e:
            return server_error(str(e))

    def get_by_id(self, entity_id):
        try:
            request = BasicGetRequestModel(entity_id)
            interactor = BasicGetInteractor(request, self.adapter_instance)
            response = interactor.run()
            if response:
                return success(response)

            objeto = self.entity_name.capitalize()
            return not_found(f'{objeto} não encontrado')
        except BaseException as e:
            return server_error(str(e))

    def post(self, json_data):
        try:
            request = BasicPostRequestModel(json_data)
            interactor = BasicPostInteractor(
                request, self.adapter_instance, self.entity_class)
            response = interactor.run()
        except SaveEntityException as e:
            return server_error(str(e))
        return created(response)

    def put(self, json_data):
        try:
            request = BasicPutRequestModel(json_data)
            interactor = BasicPutInteractor(
                request, self.adapter_instance, self.entity_class)
            response = interactor.run()
        except UpdateEntityException as e:
            return server_error(str(e))
        return success(response)

    def delete(self, entity_id):
        try:
            request = BasicDeleteRequestModel(entity_id)
            interactor = BasicDeleteInteractor(request, self.adapter_instance)
            response = interactor.run()
            if not response:
                objeto = self.entity_name.capitalize()
                return not_found(
                    f'{objeto} não encontrado para ser deletado')
            return success(response)
        except BaseException as e:
            return server_error(str(e))
