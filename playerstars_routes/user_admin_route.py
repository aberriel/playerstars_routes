from playerstars_routes.chalice_support.auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import \
    PostUserAdminInteractor, PostUserAdminRequestModel,\
    GetUserAdminRequestModel, GetUserAdminInteractor, \
    GetAllUsersAdminsInteractor, \
    SaveUserAdminException, UpdateUserAdminException, \
    PutUserAdminInteractor, PutUserAdminRequestModel
from playerstars_routes.basic_chalice_route import BasicChaliceRoute

bp_user_admin = Blueprint(__name__)


@bp_user_admin.route(
    '/user-admin/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_user_admin():
    from app import app
    data = app.current_request.json_body
    return UserAdminChaliceRoute().post(data)


@bp_user_admin.route(
    '/user-admin/{entity_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_user_admin_by_id(entity_id):
    return UserAdminChaliceRoute().get_by_id(entity_id)


@bp_user_admin.route(
    '/user-admin/', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_user_admin():
    return UserAdminChaliceRoute().get_all()


@bp_user_admin.route(
    '/user-admin/{entity_id}', methods=['PUT'], cors=cors, authorizer=cupauth)
def put_user_admin(entity_id):
    from app import app
    data = app.current_request.json_body
    return UserAdminChaliceRoute().put(data)


class UserAdminChaliceRoute(BasicChaliceRoute):

    def make_post_request(self, data):

        return PostUserAdminRequestModel(
            name=data['name'],
            email=data['email']
        )

    def make_put_request(self, data):
        return PutUserAdminRequestModel(
            user_id=data['entity_id'],
            name=data['name'],
            email=data['email']
        )

    def get_all_interactor(self):
        return GetAllUsersAdminsInteractor

    def not_found_message(self):
        return 'User Admin não encontrado'

    def not_found_all_message(self):
        return 'Nenhum user admin encontrado'

    def get_request_model(self):
        return GetUserAdminRequestModel

    def get_interactor(self):
        return GetUserAdminInteractor

    def save_exception(self):
        return SaveUserAdminException

    def post_interactor(self):
        return PostUserAdminInteractor

    def update_exception(self):
        return UpdateUserAdminException

    def put_interactor(self):
        return PutUserAdminInteractor

    def delete_request_model(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_interactor(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_not_found(self):
        return 'Player não encontrado para ser deletado'
