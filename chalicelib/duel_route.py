from chalice import Blueprint
from chalice_support import server_error, created, success, not_found, \
    bad_request
from chalicelib.chalice_support.auth import cors
from playerstars_domain import Duel, PreDuel
from playerstars_interactors import (
    CancelDuelException,
    CancelDuelInteractor,
    CancelDuelInteractorAdapters,
    CancelDuelRequestModel,
    CreateDuelException,
    CreateDuelInteractor,
    CreateDuelRequestModel,
    EndDuelException,
    EndDuelInteractor,
    EndDuelRequestModel,
    EnterDuelException,
    EnterDuelInteractor,
    EnterDuelInteractorAdapters,
    EnterDuelRequestModel,
    GetMatchListInteractor,
    GetMatchListRequestModel,
    GetOpponentCandidateListException,
    GetOpponentCandidateListInteractor,
    GetOpponentCandidateListRequestModel,
    GetAllPlayerDuelByStatusError,
    GetAllPlayerDuelByStatusInteractor,
    GetAllPlayerDuelByStatusRequestModel,
    InformOpponentResponseTimeoutException,
    GetOpponentTeamsInteractor,
    InformOpponentResponseTimeoutInteractor,
    InformOpponentResponseTimeoutInteractorAdapters,
    GetOpponentTeamsRequestModel,
    InformOpponentResponseTimeoutRequestModel,
    RejectDuelException,
    RejectDuelInteractor,
    RejectDuelRequestModel,
    GetDuelRequestModel,
    GetDuelInteractor,
    PostPreDuelInteractor,
    PostPreDuelRequestModel,
    PutPreDuelInteractor,
    PutPreDuelRequestModel,
    PutPreDuelAdapters)
from playerstars_interactors.duel.validate_photo import (
    ValidatePhotoException, ValidatePhotoInteractor,
    ValidatePhotoAdapters, ValidatePhotoRequestModel)
from playerstars_interactors.duel.end_duel import LoadDuelException, \
    LoadMemberException, UpdateDuelException, JudgeException, \
    UploadImageException, SubmitResultException
from playerstars_interactors.duel.enter_duel import InvalidStatusException

from chalicelib.aspect.logging import logger_aspect, Logging
from chalicelib.chalice_support import (
    private_get,
    private_post,
    private_put,
    private_delete)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from .basic_entity_route import BasicEntityRoute
from .duel_route_adapters import (
    get_preduel_adapter,
    get_duel_adapter_dynamo,
    get_console_adapter,
    get_duel_adapter_graphql,
    get_notification_adapter_dynamo,
    get_notification_adapter_graphql,
    get_player_adapter,
    get_team_adapter,
    get_schedule_task_adapter,
    get_aws_task_scheduler_adapter,
    get_era_adapter,
    get_values_adapter)
import logging

bp_cancel_duel = Blueprint(__name__)
bp_create_duel = Blueprint(__name__)
bp_duel = Blueprint(__name__)
bp_enter_duel = Blueprint(__name__)
bp_inform_invite_timeout = Blueprint(__name__)
bp_match_list = Blueprint(__name__)


logger = logging.getLogger()
logger.setLevel(Settings.LOG_LEVEL)
aspect_logging = Logging()
aspect_logging.set_logger(logger)


def get_preduel_router():
    return BasicEntityRoute(get_preduel_adapter(), PreDuel, 'pre-duel')


@bp_match_list.route('/', **private_get())
def get_match_list():
    data = bp_match_list.current_request.json_body
    player_id = get_user_id_from_jwt(bp_match_list)
    data.update({'player_id': player_id})
    return get_match_list_by_player(data)


@logger_aspect
def get_match_list_by_player(data):
    request = GetMatchListRequestModel(data)
    interactor = GetMatchListInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    response_data = interactor.run()()
    if response_data:
        return success(response_data)
    return not_found("Nenhum match encontrado para o player: {0}"
                     .format(data['player_id']))


@bp_create_duel.route('/', **private_post())
def post_duel():
    data = bp_create_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_create_duel)
    data.update({'challenger': entity_id})
    return create_duel(data)


@logger_aspect
def create_duel(json_data):
    try:
        request = CreateDuelRequestModel(json_data)
        interactor = CreateDuelInteractor(
            request=request,
            duel_adapter=get_duel_adapter_dynamo(),
            notification_adapter=get_notification_adapter_graphql(),
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            accept_time=Settings.TIME_TO_ACCEPT_DUEL,
            time_to_finish=Settings.TIME_TO_FINISH_DUEL)
        response = interactor.run()
    except CreateDuelException as e:
        return server_error(str(e))
    return created(response())


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


@logger_aspect
def enter_duel_post(json_data):
    request = EnterDuelRequestModel(json_data)
    adapters = EnterDuelInteractorAdapters(
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        notification_adapter=get_notification_adapter_graphql(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter(),
        era_adapter=get_era_adapter(),
        scheduler_adapter=get_aws_task_scheduler_adapter())
    interactor = EnterDuelInteractor(
        request=request,
        adapters=adapters,
        schedule_task_adapter=get_schedule_task_adapter(),
        time_to_accept_invitation=Settings.TIME_TO_ACCEPT_DUEL,
        time_to_finish_duel=Settings.TIME_TO_FINISH_DUEL,
        era_finish_duel_url=Settings.ERA_FINISH_DUEL_URL)
    try:
        response = interactor.run()

    except InvalidStatusException as e:
        return bad_request(str(e))

    except EnterDuelException as e:
        return server_error(str(e))
    return success(response())


@bp_inform_invite_timeout.route('/', **private_post())
def inform_invitation_timeout():
    data = bp_inform_invite_timeout.current_request.json_body
    player_id = get_user_id_from_jwt(bp_inform_invite_timeout)
    data.update({'player_id': player_id})
    return inform_invitation_timeout_post(data)


@logger_aspect
def inform_invitation_timeout_post(json_data):
    request = InformOpponentResponseTimeoutRequestModel(json_data)
    adapters = InformOpponentResponseTimeoutInteractorAdapters(
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    interactor = InformOpponentResponseTimeoutInteractor(
        request=request,
        adapters=adapters)

    try:
        response = interactor.run()
    except InformOpponentResponseTimeoutException as e:
        return server_error(str(e))
    return success(response())


@bp_duel.route('/get-my-duels', **private_get())
def get_all_player_duels():
    entity_id = get_user_id_from_jwt(bp_duel)
    return get_player_duels(entity_id)


@logger_aspect
def get_player_duels(player_id):
    request = GetAllPlayerDuelByStatusRequestModel(player_id)
    interactor = GetAllPlayerDuelByStatusInteractor(
        request=request,
        adapter_instance=get_duel_adapter_dynamo(),
        team_adapter=get_team_adapter(),
        player_adapter=get_player_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f"No duel found for the player {player_id}")


@bp_duel.route('/get-my-duels/{status}', **private_get())
def get_duels_by_status_route(status):
    entity_id = get_user_id_from_jwt(bp_duel)
    return get_duels_by_status(entity_id, status)


@logger_aspect
def get_duels_by_status(entity_id, status):
    request = GetAllPlayerDuelByStatusRequestModel(entity_id, status)
    interactor = GetAllPlayerDuelByStatusInteractor(
        request=request,
        adapter_instance=get_duel_adapter_dynamo(),
        team_adapter=get_team_adapter(),
        player_adapter=get_player_adapter())
    try:
        response = interactor.run()
        if response:
            return success(response)
        return not_found(
            f"No duel found with status {status} for the player {entity_id}")
    except GetAllPlayerDuelByStatusError as e:
        return server_error(str(e))


def get_duel_router():
    return BasicEntityRoute(get_duel_adapter_dynamo(), Duel, 'duel')


@bp_duel.route('/', **private_get())
@logger_aspect
def get_all_duel():
    return get_duel_router().get_all()


@bp_duel.route('/{entity_id}', **private_get())
@logger_aspect
def get_duel(entity_id):
    return get_duel_router().get_by_id(entity_id)


@bp_duel.route('/{entity_id}/details', **private_get())
@logger_aspect
def get_duel_details(entity_id):
    player_id = get_user_id_from_jwt(bp_duel)
    get_data = {
        "duel_id": entity_id,
        "player_id": player_id}
    try:
        request = GetDuelRequestModel(get_data)
        interactor = GetDuelInteractor(
            request, get_duel_adapter_dynamo(),
            get_player_adapter(), get_team_adapter())
        response = interactor.run()()
        if response:
            return success(response)
        return not_found(f'Duel: {entity_id} not found')
    except BaseException as e:
        return server_error(str(e))


@bp_duel.route('/get-opponents', **private_get())
def get_opponent_list_route():
    data = bp_duel.current_request.json_body
    player_id = get_user_id_from_jwt(bp_duel)
    data.update({'player_id': player_id})
    return get_opponent_list(data)


@logger_aspect
def get_opponent_list(data):
    request = GetOpponentCandidateListRequestModel(data)
    interactor = GetOpponentCandidateListInteractor(
        request=request,
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    try:
        response = interactor.run()()
        if response:
            return success(response)
        return not_found(f"No opponent candidate found")
    except GetOpponentCandidateListException as e:
        return server_error(str(e))


@bp_duel.route('/reject/', **private_post())
def reject_duel_route():
    data = bp_duel.current_request.json_body
    return reject_duel(data)


@logger_aspect
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
    return success(response())


@bp_duel.route('/validate-photo', methods=['POST'], cors=cors)
def validate_photo_route():
    data = bp_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_duel)
    data.update({'player_id': entity_id})
    return validate_photo(data)


@logger_aspect
def validate_photo(json_data):
    try:
        request = ValidatePhotoRequestModel(json_data)
        adapters = ValidatePhotoAdapters(
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            duel_adapter=get_duel_adapter_dynamo(),
            values_adapter=get_values_adapter()
        )
        interactor = ValidatePhotoInteractor(
            request=request,
            adapters=adapters,
            s3_bucket_name=Settings.S3_BUCKET_NAME,
            s3_bucket_url=Settings.S3_BUCKET_URL)
        response = interactor.run()
        return success(response())
    except ValidatePhotoException as e:
        msg = f'Error in validate-photo: {e.__class__.__name__}({e})'
        return server_error(msg)

    except Exception as e:
        msg = f'Unexpected error in validate-photo: ' \
            f'{e.__class__.__name__}({e})'
        return server_error(msg)


@bp_duel.route('/end-duel', methods=['POST'], cors=cors)
def end_duel():
    data = bp_duel.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_duel)
    data.update({'player_id': entity_id})
    return end_duel_post(data)


@logger_aspect
def end_duel_post(json_data):
    request = EndDuelRequestModel(json_data)
    interactor = EndDuelInteractor(
        request=request,
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        notification_adapter=get_notification_adapter_graphql(),
        player_adapter=get_player_adapter(),
        s3_bucket_name=Settings.S3_BUCKET_NAME,
        s3_bucket_url=Settings.S3_BUCKET_URL,
        team_adapter=get_team_adapter(),
        values_adapter=get_values_adapter(),
        judge_matrix=Settings.DUEL_JUDGE_MATRIX)
    try:
        response = interactor.run()
        return success(response())
    except (EndDuelException,
            LoadDuelException,
            LoadMemberException,
            UpdateDuelException,
            JudgeException,
            UploadImageException,
            SubmitResultException) as e:
        msg = f'Error in end_duel_post: {e.__class__.__name__}({e})'
        return server_error(msg)

    except Exception as e:
        msg = f'Unexpected error in end_duel: {e.__class__.__name__}({e})'
        return server_error(msg)


@bp_cancel_duel.route('/', **private_post())
def cancel_duel_route():
    data = bp_cancel_duel.current_request.json_body
    player_id = get_user_id_from_jwt(bp_cancel_duel)
    data.update({'player_id': player_id})
    return cancel_duel_post(data)


def mount_cancel_duel_interactor_adapters():
    return CancelDuelInteractorAdapters(
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        notification_adapter_dynamo=get_notification_adapter_dynamo(),
        notification_adapter_graphql=get_notification_adapter_graphql(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())


@logger_aspect
def cancel_duel_post(json_data):
    request = CancelDuelRequestModel(json_data)
    interactor = CancelDuelInteractor(
        request=request,
        adapters=mount_cancel_duel_interactor_adapters())
    try:
        response = interactor.run()
    except CancelDuelException as e:
        return server_error(str(e))
    return success(response())


@bp_duel.route('/teams/get-opponent', **private_get())
@logger_aspect
def get_opponent_teams_for_duel():
    try:
        data = bp_duel.current_request.query_params
        player_adapter = get_player_adapter()
        team_adapter = get_team_adapter()
        request = GetOpponentTeamsRequestModel(data)
        interactor = GetOpponentTeamsInteractor(
            request, player_adapter, team_adapter)
        response = interactor.run()()
        if response:
            return success(response)
        return not_found(f'No team found to be opponent of that team id')
    except BaseException as ex:
        return server_error(str(ex))


@bp_duel.route('/random/{entity_id}', **private_get())
@logger_aspect
def get_random_duel(entity_id):
    return get_preduel_router().get_by_id(entity_id)


@bp_duel.route('/random', **private_post())
@logger_aspect
def post_random_duel():
    try:
        data = bp_duel.current_request.json_body
        player_id = get_user_id_from_jwt(bp_duel)
        data.update({'player_id': player_id})
        request = PostPreDuelRequestModel(data)
        interactor = PostPreDuelInteractor(
            request, get_preduel_adapter(), get_player_adapter(),
            get_team_adapter())
        response = interactor.run()
        preduel_id, operation = response()
        if operation == 'created':
            return created(preduel_id)
        return success(preduel_id)
    except BaseException as ex:
        return server_error(str(ex))


@bp_duel.route('/random/{entity_id}/{status}', **private_put())
@logger_aspect
def put_random_duel(entity_id, status):
    try:
        player_id = get_user_id_from_jwt(bp_duel)
        data = {
            'player_id': player_id,
            'preduel_id': entity_id,
            'status': status
        }
        request = PutPreDuelRequestModel(data)
        adapters = PutPreDuelAdapters(
            preduel_adapter=get_preduel_adapter(),
            player_adapter=get_player_adapter(),
            team_adapter=get_team_adapter(),
            duel_adapter=get_duel_adapter_dynamo(),
            console_adapter=get_console_adapter(),
            notification_adapter=get_notification_adapter_graphql(),
            schedule_task_adapter=get_schedule_task_adapter(),
            era_adapter=get_era_adapter(),
            scheduler_adapter=get_aws_task_scheduler_adapter()
        )
        interactor = PutPreDuelInteractor(
            request=request,
            time_to_finish=Settings.TIME_TO_FINISH_DUEL,
            adapters=adapters,
            era_finish_duel_url=Settings.ERA_FINISH_DUEL_URL
        )
        response = interactor.run()
        return success(response())
    except BaseException as ex:
        return server_error(str(ex))


@bp_duel.route('/random/{entity_id}', **private_delete())
@logger_aspect
def delete_random_duel(entity_id):
    return get_preduel_router().delete(entity_id)
