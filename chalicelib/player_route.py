from chalice import Blueprint
from playerstars_adapters import \
    PlayerAdapter, DuelAdapter, TeamAdapter, ConsoleAdapter
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
    UpdateEntityException, PostPlayerAcceptTermsInteractor,
    PostPlayerConsoleDataInteractor, AcceptTeamInvitationInteractor,
    AcceptTeamInvitationException, AcceptTeamInvitationRequestModel,
    GetPlayersByConsoleGameRequestModel, GetPlayersByConsoleGameInteractor,
    SaveConvertedStarsInteractor, SaveConvertedStarsRequestModel,
    SaveConvertedStarsException, GetRankingByConsoleGameRequestModel,
    GetRankingByConsoleGameInteractor)
from chalicelib.team_route import get_by_user
from chalicelib.chalice_support import (
    server_error, created, success, not_found, success_partial)

bp_player = Blueprint(__name__)


def get_router():
    adapter = PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Player, 'player')


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


def get_console_adapter():
    return ConsoleAdapter(Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


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
    try:
        request = BasicPostRequestModel(json_data)
        interactor = PostPlayerInteractor(request, adapter, Player, Settings)
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
    try:
        adapter = get_adapter()
        request = UpdateProfileRequestModel(json_data)
        interactor = UpdateProfileInteractor(request, adapter, Settings)
        response = interactor.run()
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)


@bp_player.route('/{entity_id}', **private_get())
def get_player_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_player.route('/', **private_get())
def get_all_player():
    if bp_player.current_request and \
            bp_player.current_request.query_params:
        return get_player_by_console(bp_player.current_request.query_params)
    return get_router().get_all()


def get_player_by_console(query_params):
    try:
        player_adapter = get_adapter()
        console_adapter = get_console_adapter()
        request = GetPlayersByConsoleGameRequestModel(query_params)
        interactor = GetPlayersByConsoleGameInteractor(
            request, player_adapter, console_adapter)
        response = interactor.run()
        if response:
            return success(response)
        return not_found(f"Nenhum player encontrado para o console: "
                         f"{query_params.get('console_id', None)} e o game:"
                         f"{query_params.get('game_id', None)}")
    except BaseException as exc:
        return server_error(str(exc))


@bp_player.route('/get-my-profile', **private_get())
def get_my_profile():
    entity_id = get_user_id_from_jwt(bp_player)
    return get_by_id(entity_id)


def get_by_id(entity_id):
    adapter = get_adapter()
    duel_adapter = DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)
    team_adapter = get_team_adapter()
    request = GetProfileRequestModel(entity_id)
    interactor = GetProfileInteractor(
        request, adapter, team_adapter, duel_adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Player not found')

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


@bp_player.route('/friends', **private_get())
def get_friends_route_v2():
    entity_id = get_user_id_from_jwt(bp_player)
    return get_friends(entity_id)


def get_friends(entity_id):
    adapter = get_adapter()
    request = GetAllFriendsRequestModel(entity_id)
    interactor = GetAllFriendsInteractor(request, adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Favorites not found')


@bp_player.route('/{entity_id}/friends', **private_post())
def post_friend_route(entity_id):
    data = bp_player.current_request.json_body
    return alter_friend_list(entity_id, data, 'add')


@bp_player.route('/friends', **private_post())
def post_friend_route_v2():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    return alter_friend_list(entity_id, data, 'add')


@bp_player.route('/{entity_id}/friends', **private_delete())
def delete_friend_route(entity_id):
    data = bp_player.current_request.json_body
    return alter_friend_list(entity_id, data, 'delete')


@bp_player.route('/friends', **private_delete())
def delete_friend_route_v2():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
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


@bp_player.route('/my-teams/', **private_get())
def get_all_teams_from_player():
    player_id = get_user_id_from_jwt(bp_player)
    return get_by_user(player_id)


@bp_player.route('/console-data/', **private_post())
def post_console_data_route():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    data.update({'entity_id': entity_id})
    return post_console_data(data)


def post_console_data(json_data):
    adapter = get_adapter()
    console_adapter = get_console_adapter()
    request = BasicPostRequestModel(json_data)
    interactor = PostPlayerConsoleDataInteractor(
        request, adapter, console_adapter, Player)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


@bp_player.route('/accept-terms/', **private_post())
def post_accept_terms_route():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    data.update({'entity_id': entity_id})
    return post_accept_terms(data)


def post_accept_terms(json_data):
    adapter = get_adapter()
    request = BasicPostRequestModel(json_data)
    interactor = PostPlayerAcceptTermsInteractor(request, adapter, Player)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


@bp_player.route('/accept-team-invite', **private_post())
def accept_team_invitation_route():
    data = bp_player.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_player)
    data.update({'player_id': entity_id})
    return accept_team_invitation(data)


def accept_team_invitation(json_data):
    request = AcceptTeamInvitationRequestModel(json_data)
    interactor = AcceptTeamInvitationInteractor(
        request=request, team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except AcceptTeamInvitationException as e:
        return server_error(str(e))
    return success(response)


@bp_player.route('/convert-stars', **private_post())
def convert_star_route():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        data.update({'player_id': entity_id})
        request = SaveConvertedStarsRequestModel(data)
        interactor = SaveConvertedStarsInteractor(request, get_adapter())
        response = interactor.run()
    except SaveConvertedStarsException as e:
        return server_error(str(e))
    return success(response)


@bp_player.route('/ranking', **private_get())
def get_ranking_route():
    try:
        query_params = bp_player.current_request.query_params
        entity_id = get_user_id_from_jwt(bp_player)
        request = GetRankingByConsoleGameRequestModel(query_params, entity_id)
        interactor = GetRankingByConsoleGameInteractor(
            request, get_adapter(), get_console_adapter())
        response, range_data = interactor.run()
        if response:
            return success_partial(
                response, range_data.unit, range_data.initial,
                range_data.final, range_data.total)
    except BaseException as e:
        return server_error(str(e))
    return not_found(f'Player {entity_id} ranking not found')
