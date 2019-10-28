from chalice import Blueprint
from playerstars_adapters import PlayerAdapter, DuelAdapter, TeamAdapter
from playerstars_domain import Player
from chalicelib.chalice_support import (
    private_get, private_post, private_delete, private_put)

from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

from playerstars_interactors import (
    BasicPostRequestModel, PostPlayerInteractor, SaveEntityException,
    GetAllFriendsInteractor, GetAllFriendsRequestModel, AlterFriendsInteractor,
    AlterFriendsRequestModel, SaveFriendsException, GetProfileInteractor,
    GetProfileRequestModel, UpdateProfileRequestModel, UpdateProfileInteractor,
    UpdateEntityException)

from chalicelib.chalice_support import (
    server_error, created, success, not_found)

bp_player = Blueprint(__name__)


def get_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


def get_adapter():
    return PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_player.route('/', **private_post())
def post_player():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    data.update({'entity_id': entity_id})
    return post(data)


def post(json_data):
    adapter = get_adapter()
    request = BasicPostRequestModel(json_data)
    interactor = PostPlayerInteractor(request, adapter, Player)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


@bp_player.route('/', **private_put())
def put_player():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    data.update({'entity_id': entity_id})
    return put(data)


def put(json_data):
    adapter = get_adapter()
    request = UpdateProfileRequestModel(json_data)
    interactor = UpdateProfileInteractor(request, adapter)
    try:
        response = interactor.run()
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)


@bp_player.route('/{entity_id}', **private_get())
def get_player_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_player.route('/', **private_get())
def get_all_player():
    return get_router().get_all()


@bp_player.route('/get-my-profile', **private_get())
def get_my_profile():
    entity_id = get_user_id_from_jwt(bp_player)
    return get_by_id(entity_id)


def get_by_id(entity_id):
    adapter = get_adapter()
    duel_adapter = DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)
    team_adapter = TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)
    request = GetProfileRequestModel(entity_id)
    interactor = GetProfileInteractor(
        request, adapter, team_adapter, duel_adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Player não encontrado')

# player/<Id>/friends
# POST
# GET
# player/<Id>/friend/<id>
# PUT
# DELETE
#
#
# Talvez um meio termo seria ter um:
# /player/<id>/friends POST/PUT
# Recebendo uma lista


@bp_player.route('/{entity_id}/friends', **private_get())
def get_friends_route(entity_id):
    return get_friends(entity_id)


def get_friends(entity_id):
    adapter = get_adapter()
    request = GetAllFriendsRequestModel(entity_id)
    interactor = GetAllFriendsInteractor(request, adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Favoritos não enontrados')


@bp_player.route('/{entity_id}/friends', **private_post())
def post_friend_route(entity_id):
    data = bp_player.current_request.json_body
    return alter_friend_list(entity_id, data, 'add')


@bp_player.route('/{entity_id}/friends', **private_delete())
def delete_friend_route(entity_id):
    data = bp_player.current_request.json_body
    return alter_friend_list(entity_id, data, 'delete')


def alter_friend_list(entity_id, data, option):
    adapter = get_adapter()
    request = AlterFriendsRequestModel(player_id=entity_id, list_entity_id=data['friends'])
    interactor = AlterFriendsInteractor(request, adapter, option)
    try:
        response = interactor.run()
    except SaveFriendsException as e:
        return server_error(str(e))
    return created(response)
