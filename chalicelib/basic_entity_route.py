from playerstars_interactors import (
    BasicGetRequestModel, BasicGetInteractor,
    BasicPostRequestModel, BasicPostInteractor, SaveEntityException,
    BasicPutRequestModel, BasicPutInteractor, UpdateEntityException,
    BasicDeleteInteractor, BasicDeleteRequestModel
)
from clapy_basic_classes.basic_interactors.basic_get_all import (
    BasicGetAllInteractor, BasicGetAllRequestModel
)
from chalice_support.api_responses import (
    created, not_found, server_error, success, success_partial)
from marshmallow import ValidationError


class BasicEntityRoute:
    def __init__(self, adapter_instance, entity_class, entity_name='objeto'):
        self.adapter_instance = adapter_instance
        self.entity_class = entity_class
        self.entity_name = entity_name

    def get_all(self, query_params=None, unit=None):
        try:
            request = BasicGetAllRequestModel(query_params, unit)
            interactor = BasicGetAllInteractor(request, self.adapter_instance)
            response = interactor.run()

            return success_partial(response.object_list,
                                   response.unit,
                                   response.initial,
                                   response.final,
                                   response.total)
        except ValidationError as e:
            msg = f'Validation error obtaining list of ' \
                  f'{self.entity_name}: {e}'
            return server_error(msg)
        except BaseException as e:
            msg = f'Error obtaining list of {self.entity_name}: {e}'
            return server_error(msg)

    def get_by_id(self, entity_id):
        try:
            request = BasicGetRequestModel(entity_id)
            interactor = BasicGetInteractor(request, self.adapter_instance)
            response = interactor.run()
            if response:
                return success(response)

            objeto = self.entity_name.capitalize()
            return not_found(f'{objeto} not found')
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
                    f'{objeto} not found to be deleted')
            return success(response)
        except BaseException as e:
            return server_error(str(e))
