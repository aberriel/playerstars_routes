from playerstars_interactors import BasicGetAllInteractor
from playerstars_interactors import BasicGetRequestModel, BasicGetInteractor
from playerstars_interactors import (BasicPostRequestModel,
                                     BasicPostInteractor, SaveEntityException)
from playerstars_interactors import (BasicPutRequestModel, BasicPutInteractor,
                                     UpdateEntityException)
from playerstars_interactors import (BasicDeleteInteractor,
                                     BasicDeleteRequestModel)

from playerstars_routes.chalice_support.api_responses import (success,
                                                              not_found,
                                                              server_error,
                                                              created)


class BasicEntityRoute:
    def __init__(self, adapter_instance, entity_class, entity_name='objeto'):
        self.adapter_instance = adapter_instance
        self.entity_class = entity_class
        self.entity_name = entity_name

    @staticmethod
    def capitalize(name):
        return name[0].upper() + name[1:]

    def get_all(self):
        interactor = BasicGetAllInteractor(self.adapter_instance)
        response = interactor.run()
        if response:
            return success(response)
        return not_found(f'Nenhum {self.entity_name} encontrado')

    def get_by_id(self, entity_id):
        request = BasicGetRequestModel(entity_id)
        interactor = BasicGetInteractor(request, self.adapter_instance)
        response = interactor.run()
        if response:
            return success(response)

        objeto = self.capitalize(self.entity_name)
        return not_found(f'{objeto} não encontrado')

    def post(self, json_data):
        request = BasicPostRequestModel(json_data)
        interactor = BasicPostInteractor(request,
                                         self.adapter_instance,
                                         self.entity_class)
        try:
            response = interactor.run()
        except SaveEntityException as e:
            return server_error(str(e))
        return created(response)

    def put(self, json_data):
        request = BasicPutRequestModel(json_data)
        interactor = BasicPutInteractor(request,
                                        self.adapter_instance,
                                        self.entity_class)
        try:
            response = interactor.run()
        except UpdateEntityException as e:
            return server_error(str(e))
        return success(response)

    def delete(self, entity_id):
        request = BasicDeleteRequestModel(entity_id)
        interactor = BasicDeleteInteractor(request, self.adapter_instance)
        response = interactor.run()
        if not response:
            objeto = self.capitalize(self.entity_name)
            return not_found(f'{objeto} não encontrado para '
                             f'ser deletado')
        return success(response)
