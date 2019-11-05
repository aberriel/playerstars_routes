from chalice import Blueprint

from playerstars_adapters import DuelAdapter, PlayerAdapter
from .basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
from playerstars_domain import Duel
from chalicelib.chalice_support import \
    private_get, private_post, server_error, created, success, not_found
from playerstars_interactors import (
    CreateDuelInteractor, CreateDuelRequestModel, CreateDuelException,
    EnterDuelException, EnterDuelInteractor, EnterDuelRequestModel,
    GetAllPlayerDuelRequestModel, GetAllPlayerDuelInteractor,
    GetMatchListInteractor, GetMatchListRequestModel,
    GetPlayerDuelByStatusInteractor, GetPlayerDuelByStatusRequestModel,
    GetPlayerDuelByStatusError)
from chalicelib.utils import get_user_id_from_jwt


bp_match_list = Blueprint(__name__)
bp_create_duel = Blueprint(__name__)
bp_enter_duel = Blueprint(__name__)
bp_duel = Blueprint(__name__)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_match_list.route('/', **private_get())
def get_match_list():
    entity_id = get_user_id_from_jwt(bp_match_list)
    return get_match_list_by_player(entity_id)


def get_match_list_by_player(entity_id):
    request = GetMatchListRequestModel(entity_id)
    interactor = GetMatchListInteractor(request, get_player_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum match encontrado para o player: " + entity_id)


def get_duel_adapter():
    return DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_create_duel.route('/', **private_post())
def post_duel():
    data = bp_create_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_create_duel)
    data.update({'challenger_id': entity_id})
    return create_duel(data)


def create_duel(json_data):
    request = CreateDuelRequestModel(json_data)

    interactor = CreateDuelInteractor(
        request=request, player_adapter=get_player_adapter(),
        duel_adapter=get_duel_adapter(), settings=Settings)
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
        request=request, player_adapter=get_player_adapter(),
        duel_adapter=get_duel_adapter()
    )
    try:
        response = interactor.run()
    except EnterDuelException as e:
        return server_error(str(e))
    return success(response)


@bp_duel.route('/get-my-duels', **private_get())
def get_all_player_duels():
    entity_id = get_user_id_from_jwt(bp_duel)
    return get_player_duels(entity_id)


def get_player_duels(player_id):
    request = GetAllPlayerDuelRequestModel(player_id)
    interactor = GetAllPlayerDuelInteractor(request, get_duel_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f"Nenhum duel encontrado para o player: {player_id}")


def get_duel_router():
    return BasicEntityRoute(get_duel_adapter(), Duel, 'duel')


@bp_duel.route('/', **private_get())
def get_all_duel():
    return get_duel_router().get_all()


@bp_duel.route('/{entity_id}', **private_get())
def get_duel(entity_id):
    return get_duel_router().get_by_id(entity_id)


@bp_duel.route('/get-my-duels/{status}', **private_get())
def get_duels_by_status_route(status):
    entity_id = get_user_id_from_jwt(bp_duel)
    return get_duels_by_status(entity_id, status)


def get_duels_by_status(entity_id, status):
    request = GetPlayerDuelByStatusRequestModel(entity_id, status)
    interactor = GetPlayerDuelByStatusInteractor(request, get_duel_adapter())
    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found(
            f"Nenhum duelo com o status: {status} encontrado para"
            f" o player: {entity_id}")
    except GetPlayerDuelByStatusError as e:
        return server_error(str(e))
