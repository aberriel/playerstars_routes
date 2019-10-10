from chalice import Blueprint

from playerstars_adapters import DuelAdapter, PlayerAdapter
from .basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
from playerstars_domain import Player, Duel
from chalicelib.chalice_support import \
    private_get, private_post, server_error, created, success, not_found
from playerstars_interactors import (
    CreateDuelInteractor, CreateDuelRequestModel, CreateDuelException,
    EnterDuelException, EnterDuelInteractor, EnterDuelRequestModel,
    GetAllPlayerDuelRequestModel, GetAllPlayerDuelInteractor)
from chalicelib.utils import get_user_id_from_jwt


bp_match_list = Blueprint(__name__)
bp_create_duel = Blueprint(__name__)
bp_enter_duel = Blueprint(__name__)
bp_duel = Blueprint(__name__)


def get_router_match_list():
    return BasicEntityRoute(get_player_adapter(), Player, 'player')


@bp_match_list.route('/{user_id}', **private_get())
def get_match_list(user_id):
    return get_router_match_list().get_by_id(user_id)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def get_duel_adapter():
    return DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_create_duel.route('/', **private_post())
def post_duel():
    data = bp_create_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_create_duel)
    data.update({'player_id': entity_id})
    return create_duel(data)


def create_duel(json_data):
    request = CreateDuelRequestModel(json_data)
    interactor = CreateDuelInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        duel_adapter=get_duel_adapter())
    try:
        response = interactor.run()
    except CreateDuelException as e:
        return server_error(str(e))
    return created(response)


@bp_enter_duel.route('/', **private_post())
def enter_duel():
    data = bp_enter_duel.current_request.json_body
    return enter_duel_post(data)


def enter_duel_post(json_data):
    request = EnterDuelRequestModel(json_data)
    interactor = EnterDuelInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        duel_adapter=get_duel_adapter()
    )
    try:
        response = interactor.run()
    except EnterDuelException as e:
        return server_error(str(e))
    return success(response)


@bp_duel.route('/player/{entity_id}', **private_get())
def get_all_player_duels(entity_id):
    return get_player_duels(entity_id)


def get_player_duels(player_id):
    request = GetAllPlayerDuelRequestModel(player_id)
    interactor = GetAllPlayerDuelInteractor(request, get_duel_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum duel não encontrado para o player")


def get_all_duel_router():
    return BasicEntityRoute(get_duel_adapter(), Duel, 'duel')


@bp_duel.route('/', **private_get())
def get_all_duel():
    return get_all_duel_router().get_all()
