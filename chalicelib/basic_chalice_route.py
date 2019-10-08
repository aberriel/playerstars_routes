from abc import abstractmethod
from chalice import Blueprint


root = Blueprint(__name__)


class BasicChaliceRoute:
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
