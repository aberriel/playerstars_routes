from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import GetMatchListRequestModel, \
    GetMatchListInteractor, CreateDuelException, CreateDuelInteractor, \
    CreateDuelRequestModel, EnterDuelRequestModel, \
    EnterDuelInteractor, EnterDuelException
from playerstars_routes.basic_chalice_route import BasicChaliceRoute
from playerstars_routes.chalice_support import server_error, success
bp_duel = Blueprint(__name__)


@bp_duel.route(
    '/match-list/{user_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_match_list(user_id):
    return MatchListChaliceRoute().get_by_id(user_id)


@bp_duel.route(
    '/create-duel/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_duel():
    from app import app
    data = app.current_request.json_body
    return MatchListChaliceRoute().post(data)


@bp_duel.route(
    '/enter-duel/', methods=['POST'], cors=cors, authorizer=cupauth)
def enter_duel():
    from app import app
    data = app.current_request.json_body
    return MatchListChaliceRoute().enter_duel(data)


class MatchListChaliceRoute(BasicChaliceRoute):

    @staticmethod
    def enter_duel(data):
        request = EnterDuelRequestModel(
            player_id=data['player_id'],
            duel_id=data['duel_id'])
        interactor = EnterDuelInteractor(request)
        try:
            response = interactor.run()
        except EnterDuelException as e:
            return server_error(str(e))
        return success(response)

    def make_post_request(self, data):
        return CreateDuelRequestModel(
            player_id=data['player_id'])

    def make_put_request(self, data):
        raise NotImplementedError('Não implementado')

    def get_all_interactor(self):
        raise NotImplementedError('Não implementado')

    def not_found_message(self):
        return 'Nenhum match encontrado'

    def not_found_all_message(self):
        return 'Não implementado'

    def get_request_model(self):
        return GetMatchListRequestModel

    def get_interactor(self):
        return GetMatchListInteractor

    def save_exception(self):
        return CreateDuelException

    def post_interactor(self):
        return CreateDuelInteractor

    def update_exception(self):
        raise NotImplementedError('Não implementado')

    def put_interactor(self):
        raise NotImplementedError('Não implementado')

    def delete_request_model(self):
        raise NotImplementedError('Não implementado')

    def delete_interactor(self):
        raise NotImplementedError('Não implementado')

    def delete_not_found(self):
        raise NotImplementedError('Não implementado')
