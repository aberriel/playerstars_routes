from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import \
    PostPlayerRequestModel, PostPlayerInteractor, SavePlayerException, \
    GetPlayerInteractor, GetPlayerRequestModel, \
    GetAllPlayersInteractor
from playerstars_routes.basic_route import BasicChaliceRoute

bp_player = Blueprint(__name__)


@bp_player.route(
    '/player/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_player():
    from app import app
    data = app.current_request.json_body
    return PlayerChaliceRoute().post(data)


@bp_player.route(
    '/player/{entity_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_player_by_id(entity_id):
    return PlayerChaliceRoute().get_by_id(entity_id)


@bp_player.route(
    '/player/', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_player():
    return PlayerChaliceRoute().get_all()


class PlayerChaliceRoute(BasicChaliceRoute):

    def make_post_request(self, data):

        return PostPlayerRequestModel(
            name=data['name'],
            nickname=data['nickname'],
            birth_date=data['birth_date'],
            cpf=data['cpf'],
            email=data['email'],
            phone_number=data['phone_number'],
            street=data['street'],
            street_number=data['street_number'],
            street_complement=data['street_complement'],
            neighborhood=data['neighborhood'],
            city=data['city'],
            state=data['state'],
            country=data['country'],
            postal_code=data['postal_code'],
            promo_code=data['promo_code'],
            consoles=data['consoles'],
            favorites=data['favorites'],
            blue_star_balance=data['blue_star_balance'],
            golden_star_balance=data['golden_star_balance']
        )

    def make_put_request(self, data):
        raise NotImplementedError('Não implementado no interactor')

    def get_all_interactor(self):
        return GetAllPlayersInteractor

    def not_found_message(self):
        return 'Player não encontrado'

    def not_found_all_message(self):
        return 'Nenhum player encontrado'

    def get_request_model(self):
        return GetPlayerRequestModel

    def get_interactor(self):
        return GetPlayerInteractor

    def save_exception(self):
        return SavePlayerException

    def post_interactor(self):
        return PostPlayerInteractor

    def update_exception(self):
        raise NotImplementedError('Não implementado no interactor')

    def put_interactor(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_request_model(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_interactor(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_not_found(self):
        return 'Player não encontrado para ser deletado'
