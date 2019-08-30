from abc import abstractmethod

from chalice import Blueprint

from playerstars_routes.chalice_support import (success, not_found,
                                                server_error, created)


root = Blueprint(__name__)


class BasicChaliceRoute:

    def get_all(self):
        response = self.get_all_interactor().run()
        if response:
            return success(response)
        return not_found(self.not_found_all_message())

    def get_by_id(self, entity_id):
        request = self.get_request_model()(entity_id)
        interactor = self.get_interactor()(request)
        response = interactor.run()
        if response:
            return success(response)
        return not_found(self.not_found_message())

    def post(self, data):
        request = self.make_post_request(data)
        interactor = self.post_interactor()(request)
        try:
            response = interactor.run()
        except self.save_exception() as e:
            return server_error(str(e))
        return created(response)

    def put(self, data):
        request = self.make_put_request(data)
        interactor = self.put_interactor()(request)
        try:
            response = interactor.run()
        except self.update_exception() as e:
            return server_error(str(e))
        return success(response)

    @abstractmethod
    def make_post_request(self, data):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def get_all_interactor(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def not_found_message(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def not_found_all_message(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def get_request_model(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def get_interactor(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def save_exception(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def post_interactor(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def make_put_request(self, data):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def update_exception(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def put_interactor(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def delete_request_model(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def delete_interactor(self):
        raise NotImplementedError('Não foi implementado')

    @abstractmethod
    def delete_not_found(self):
        raise NotImplementedError('Não foi implementado')
