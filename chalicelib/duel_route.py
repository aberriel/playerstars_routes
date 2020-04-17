from .basic_entity_route import BasicEntityRoute
from chalice import Blueprint
from chalicelib.chalice_support import private_get, private_post
from chalicelib.settings import Settings
from chalice_support import server_error, created, success, not_found
from playerstars_adapters import (
    DuelAdapter as DuelAdapterDynamo,
    PlayerAdapter,
    TeamAdapter)
from playerstars_domain import Duel
from playerstars_graphql_adapters import (
    DuelAdapter as DuelAdapterGraphql,
    NotificationAdapter)
from playerstars_interactors import (
    CreateDuelException,
    CreateDuelInteractor,
    CreateDuelRequestModel,
    EndDuelException,
    EndDuelInteractor,
    EndDuelRequestModel,
    EnterDuelException,
    EnterDuelInteractor,
    EnterDuelRequestModel,
    GetAllPlayerDuelInteractor,
    GetAllPlayerDuelRequestModel,
    GetMatchListInteractor,
    GetMatchListRequestModel,
    GetOpponentCandidateListException,
    GetOpponentCandidateListInteractor,
    GetOpponentCandidateListRequestModel,
    GetPlayerDuelByStatusError,
    GetPlayerDuelByStatusInteractor,
    GetPlayerDuelByStatusRequestModel,
    InformOpponentResponseTimeoutException,
    InformOpponentResponseTimeoutInteractor,
    InformOpponentResponseTimeoutRequestModel,
    RejectDuelException,
    RejectDuelInteractor,
    RejectDuelRequestModel)
from chalicelib.utils import get_user_id_from_jwt


bp_create_duel = Blueprint(__name__)
bp_duel = Blueprint(__name__)
bp_enter_duel = Blueprint(__name__)
bp_inform_invite_timeout = Blueprint(__name__)
bp_match_list = Blueprint(__name__)


def get_duel_adapter_dynamo():
    return DuelAdapterDynamo(Settings.DUEL_TABLE_NAME,
                             Settings.DYNAMODB_URL)


def get_duel_adapter_graphql():
    return DuelAdapterGraphql(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION)


def get_notification_adapter():
    return NotificationAdapter(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.NOTIFICATION_MUTATION_NAME_PART)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME,
                         Settings.DYNAMODB_URL)


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_match_list.route('/', **private_get())
def get_match_list():
    data = bp_match_list.current_request.json_body
    player_id = get_user_id_from_jwt(bp_match_list)
    data.update({'player_id': player_id})
    return get_match_list_by_player(data)


def get_match_list_by_player(data):
    request = GetMatchListRequestModel(data)
    interactor = GetMatchListInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found("Nenhum match encontrado para o player: {0}"
                     .format(data['player_id']))


@bp_create_duel.route('/', **private_post())
def post_duel():
    data = bp_create_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_create_duel)
    data.update({'challenger': entity_id})
    return create_duel(data)


def create_duel(json_data):
    try:
        request = CreateDuelRequestModel(json_data)
        interactor = CreateDuelInteractor(
            request=request,
            duel_adapter=get_duel_adapter_dynamo(),
            notification_adapter=get_notification_adapter(),
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            settings=Settings)
        response = interactor.run()
    except CreateDuelException as e:
        return server_error(str(e))
    return created(response)


@bp_enter_duel.route('/', **private_post())
def enter_duel():
    data = bp_enter_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_enter_duel)
    data.update({'player_id': entity_id})
    data.update({
        'lambda_function_name': Settings.DUEL_SCHEDULED_FINISHER_NAME
    })
    data.update({'aws_region': Settings.AWS_DEFAULT_REGION})
    data.update({'time_to_finish': int(Settings.TIME_TO_FINISH_DUEL)})

    return enter_duel_post(data)


def enter_duel_post(json_data):
    request = EnterDuelRequestModel(json_data)
    interactor = EnterDuelInteractor(
        request=request,
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        notification_adapter=get_notification_adapter(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except EnterDuelException as e:
        return server_error(str(e))
    return success(response)


@bp_inform_invite_timeout.route('/', **private_post())
def inform_invitation_timeout():
    data = bp_inform_invite_timeout.current_request.json_body
    player_id = get_user_id_from_jwt(bp_inform_invite_timeout)
    data.update({'player_id': player_id})
    return inform_invitation_timeout_post(data)


def inform_invitation_timeout_post(json_data):
    request = InformOpponentResponseTimeoutRequestModel(json_data)
    interactor = InformOpponentResponseTimeoutInteractor(
        request=request,
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())

    try:
        response = interactor.run()
    except InformOpponentResponseTimeoutException as e:
        return server_error(str(e))
    return success(response)


@bp_duel.route('/get-my-duels', **private_get())
def get_all_player_duels():
    entity_id = get_user_id_from_jwt(bp_duel)
    return get_player_duels(entity_id)


def get_player_duels(player_id):
    request = GetAllPlayerDuelRequestModel(player_id)
    interactor = GetAllPlayerDuelInteractor(
        request=request,
        adapter_instance=get_duel_adapter_dynamo())
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f"No duel found for the player {player_id}")


def get_duel_router():
    return BasicEntityRoute(get_duel_adapter_dynamo(), Duel, 'duel')


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
    interactor = GetPlayerDuelByStatusInteractor(
        request=request,
        duel_adapter=get_duel_adapter_dynamo(),
        player_adapter=get_player_adapter())
    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found(
            f"No duel found with status {status} for the player {entity_id}")
    except GetPlayerDuelByStatusError as e:
        return server_error(str(e))


@bp_duel.route('/get-opponents', **private_get())
def get_opponent_list_route():
    data = bp_duel.current_request.json_body
    player_id = get_user_id_from_jwt(bp_duel)
    data.update({'player_id': player_id})
    return get_opponent_list(data)


def get_opponent_list(data):
    request = GetOpponentCandidateListRequestModel(data)
    interactor = GetOpponentCandidateListInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found(f"No opponent candidate found")
    except GetOpponentCandidateListException as e:
        return server_error(str(e))


@bp_duel.route('/reject/', **private_post())
def reject_duel_route():
    data = bp_duel.current_request.json_body
    return reject_duel(data)


def reject_duel(data):
    request = RejectDuelRequestModel(data)
    interactor = RejectDuelInteractor(
        request=request,
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql())
    try:
        response = interactor.run()
    except RejectDuelException as e:
        return server_error(str(e))
    return success(response)


@bp_duel.route('/end-duel', **private_post())
def end_duel():
    data = bp_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_duel)
    data.update({'player_id': entity_id})
    return end_duel_post(data)


def end_duel_post(json_data):
    request = EndDuelRequestModel(json_data)
    interactor = EndDuelInteractor(
        request=request,
        duel_adapter=get_duel_adapter_dynamo(),
        notification_adapter=get_notification_adapter(),
        player_adapter=get_player_adapter(),
        s3_bucket_name=Settings.S3_BUCKET_NAME,
        s3_bucket_url=Settings.S3_BUCKET_URL,
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()
    except EndDuelException as e:
        return server_error(str(e))
    return success(response)
