from chalice import Blueprint
from chalice_support import (
    created, not_found, server_error, success, success_partial)
from playerstars_adapters import (
    ConsoleAdapter, DuelAdapter, PlayerAdapter, TeamAdapter)
from playerstars_domain import Player
from playerstars_interactors import (
    AcceptTeamInvitationException, AcceptTeamInvitationInteractor,
    AcceptTeamInvitationRequestModel, AlterFriendsInteractor,
    AlterFriendsRequestModel, BasicPostRequestModel,
    GetAllFriendsInteractor, GetAllFriendsRequestModel,
    GetPlayersByConsoleGameInteractor, GetPlayersByConsoleGameRequestModel,
    GetProfileInteractor, GetProfileRequestModel,
    GetRankingByConsoleGameInteractor, GetRankingByConsoleGameRequestModel,
    PostPlayerAcceptTermsInteractor, PostPlayerConsoleDataInteractor,
    PostPlayerInteractor, SaveConvertedStarsException,
    SaveConvertedStarsInteractor, SaveConvertedStarsRequestModel,
    SaveEntityException, SaveFriendsException, UpdateEntityException,
    UpdateProfileInteractor, UpdateProfileRequestModel,
    GetPlayerConsolesRequestModel, GetPlayerConsolesInteractor,
    GetFriendsByConsoleGameInteractor, GetFriendsByConsoleGameRequestModel)

from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.chalice_support import (
    private_get, private_post, private_delete, private_put)
from chalicelib.settings import Settings
from chalicelib.team_route import get_by_user
from chalicelib.utils import get_user_id_from_jwt

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
        interactor = PostPlayerInteractor(
            request=request,
            adapter_instance=adapter,
            console_adapter=get_console_adapter(),
            entity_class=Player,
            s3_bucket_name=Settings.S3_BUCKET_NAME,
            s3_bucket_url=Settings.S3_BUCKET_URL)
        response = interactor.run()
        return created(response)
    except SaveEntityException as e:
        return server_error(str(e))


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
        interactor = UpdateProfileInteractor(
            request=request,
            player_adapter=adapter,
            s3_bucket_name=Settings.S3_BUCKET_NAME,
            s3_bucket_url=Settings.S3_BUCKET_URL)
        response = interactor.run()
    except UpdateEntityException as e:
        return server_error(str(e))
    return success(response)


@bp_player.route('/{entity_id}', **private_get())
def get_player_by_id(entity_id):
    return get_router().get_by_id(entity_id)


@bp_player.route('/', **private_get())
def get_all_player():
    if bp_player.current_request and bp_player.current_request.query_params:
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
    try:
        entity_id = get_user_id_from_jwt(bp_player)
        adapter = get_adapter()
        duel_adapter = DuelAdapter(
            Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)
        team_adapter = get_team_adapter()
        console_adapter = get_console_adapter()
        request = GetProfileRequestModel(entity_id)
        interactor = GetProfileInteractor(
            request, adapter, team_adapter, duel_adapter, console_adapter)
        response = interactor.run()
        if response:
            return success(response)
        return not_found(f'Player not found')
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/{entity_id}/friends', **private_get())
def get_friends_route(entity_id):
    try:
        return get_friends(entity_id)
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/friends', **private_get())
def get_friends_route_v2():
    try:
        entity_id = get_user_id_from_jwt(bp_player)
        return get_friends(entity_id)
    except BaseException as e:
        return server_error(str(e))


def get_friends(entity_id):
    adapter = get_adapter()
    request = GetAllFriendsRequestModel(entity_id)
    interactor = GetAllFriendsInteractor(request, adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Favorites not found')


@bp_player.route('/friends-by-console', **private_get())
def get_friends_by_console_game_route():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        data.update({'entity_id': entity_id})
        return get_friends_by_console(data)
    except BaseException as e:
        return server_error(str(e))


def get_friends_by_console(query_params):
    player_adapter = get_adapter()
    console_adapter = get_console_adapter()
    request = GetFriendsByConsoleGameRequestModel(query_params)
    interactor = GetFriendsByConsoleGameInteractor(
        request, player_adapter, console_adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f"Nenhum amigo encontrado para o console: "
                     f"{query_params.get('console_id', None)} e o game:"
                     f"{query_params.get('game_id', None)}")


@bp_player.route('/{entity_id}/friends', **private_post())
def post_friend_route(entity_id):
    try:
        data = bp_player.current_request.json_body
        return alter_friend_list(entity_id, data, 'add')
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/friends', **private_post())
def post_friend_route_v2():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        return alter_friend_list(entity_id, data, 'add')
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/{entity_id}/friends', **private_delete())
def delete_friend_route(entity_id):
    try:
        data = bp_player.current_request.json_body
        return alter_friend_list(entity_id, data, 'delete')
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/friends', **private_delete())
def delete_friend_route_v2():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        return alter_friend_list(entity_id, data, 'delete')
    except BaseException as e:
        return server_error(str(e))


def alter_friend_list(entity_id, data, option):
    try:
        adapter = get_adapter()
        request = AlterFriendsRequestModel(player_id=entity_id,
                                           list_entity_id=data['friends'])
        interactor = AlterFriendsInteractor(request, adapter, option)
        response = interactor.run()
    except SaveFriendsException as e:
        return server_error(str(e))
    return created(response)


@bp_player.route('/my-teams/', **private_get())
def get_all_teams_from_player():
    try:
        data = bp_player.current_request.query_params
        player_id = get_user_id_from_jwt(bp_player)
        if not data:
            data = dict()
        data.update({'player_id': player_id})
        return get_by_user(data)
    except BaseException as e:
        return server_error(str(e))


@bp_player.route('/console-data/', **private_post())
def post_console_data_route():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        data.update({'entity_id': entity_id})
        return post_console_data(data)
    except BaseException as e:
        return server_error(str(e))


def post_console_data(json_data):
    try:
        adapter = get_adapter()
        console_adapter = get_console_adapter()
        request = BasicPostRequestModel(json_data)
        interactor = PostPlayerConsoleDataInteractor(
            request, adapter, console_adapter, Player)
        response = interactor.run()
        return created(response)
    except SaveEntityException as e:
        return server_error(str(e))


@bp_player.route('/accept-terms/', **private_post())
def post_accept_terms_route():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        data.update({'entity_id': entity_id})
        return post_accept_terms(data)
    except BaseException as e:
        return server_error(str(e))


def post_accept_terms(json_data):
    try:
        adapter = get_adapter()
        request = BasicPostRequestModel(json_data)
        interactor = PostPlayerAcceptTermsInteractor(request, adapter, Player)
        response = interactor.run()
        return created(response)
    except SaveEntityException as e:
        return server_error(str(e))


@bp_player.route('/accept-team-invite', **private_post())
def accept_team_invitation_route():
    try:
        data = bp_player.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_player)
        data.update({'player_id': entity_id})
        return accept_team_invitation(data)
    except BaseException as e:
        return server_error(str(e))


def accept_team_invitation(json_data):
    try:
        request = AcceptTeamInvitationRequestModel(json_data)
        interactor = AcceptTeamInvitationInteractor(
            request=request, team_adapter=get_team_adapter())
        response = interactor.run()
        return success(response)
    except AcceptTeamInvitationException as e:
        return server_error(str(e))


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


@bp_player.route('/consoles', **private_get())
def get_player_consoles():
    try:
        entity_id = get_user_id_from_jwt(bp_player)
        request = GetPlayerConsolesRequestModel(entity_id)
        interactor = GetPlayerConsolesInteractor(
            request, get_adapter(), get_console_adapter())
        response = interactor.run()
        if response:
            return success(response)
    except BaseException as e:
        return server_error(str(e))
    return not_found(f'Player {entity_id} consoles not found')
