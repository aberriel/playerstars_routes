from chalice import Blueprint
from playerstars_adapters import (
    NotificationAdapter as NotificationAdapterDynamo,
    PlayerAdapter)
from playerstars_domain import Notification
from playerstars_graphql_adapters import \
    NotificationAdapter as NotificationAdapterGraphql
from playerstars_interactors import (
    BasicPostRequestModel,
    GetAppNotificationByUserInteractor,
    GetAppNotificationByUserRequestModel,
    PostAppNotificationInteractor,
    SaveEntityException,
    SetNotificationAsReadException,
    SetNotificationAsReadInteractor,
    SetNotificationAsReadRequestModel)
from playerstars_interactors.notification import (
    PostPlayerSnsEndpointException,
    PostPlayerSnsEndpointInteractor,
    PostPlayerSnsEndpointRequestModel)
from chalicelib.chalice_support import private_post, private_get
from chalice_support import (server_error, created, success, not_found)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

bp_notification = Blueprint(__name__)
bp_notification_read = Blueprint(__name__)


def get_notification_adapter_dynamo():
    return NotificationAdapterDynamo(Settings.NOTIFICATION_TABLE_NAME,
                                     Settings.DYNAMODB_URL)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME,
                         Settings.DYNAMODB_URL)


def get_notification_adapter_graphql():
    return NotificationAdapterGraphql(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.NOTIFICATION_MUTATION_NAME_PART)


@bp_notification.route('/', **private_post())
def post_app_notification():
    data = bp_notification.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_notification)
    data.update({'player_id': entity_id})
    return post(data)


def post(json_data):
    adapter = get_notification_adapter_dynamo()
    request = BasicPostRequestModel(json_data)
    interactor = PostAppNotificationInteractor(request, adapter, Notification)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return created(response)


@bp_notification.route('/', **private_get())
def get_app_notification():
    entity_id = get_user_id_from_jwt(bp_notification)
    return get_by_user_and_status(entity_id, None)


@bp_notification.route('/{status}', **private_get())
def get_app_notification_by_status(status):
    entity_id = get_user_id_from_jwt(bp_notification)
    return get_by_user_and_status(entity_id, status)


def get_by_user_and_status(entity_id, status):
    notification_adapter = get_notification_adapter_dynamo()
    request = GetAppNotificationByUserRequestModel(entity_id, status)
    interactor = GetAppNotificationByUserInteractor(
        request=request,
        adapter_instance=notification_adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'No notifications found for player id:'
                     f' {entity_id}')


@bp_notification_read.route('/', **private_post())
def post_set_notification_as_read():
    data = bp_notification_read.current_request.json_body
    player_id = get_user_id_from_jwt(bp_notification_read)
    data.update({'player_id': player_id})

    dynamo_adapter = get_notification_adapter_dynamo()
    graphql_adapter = get_notification_adapter_graphql()
    request = SetNotificationAsReadRequestModel(data)
    interactor = SetNotificationAsReadInteractor(
        request=request,
        notification_adapter_dynamo=dynamo_adapter,
        notification_adapter_graphql=graphql_adapter)
    try:
        response = interactor.run()
    except SetNotificationAsReadException as e:
        return server_error(str(e))
    return success(response)


@bp_notification.route('/update-user-push-endpoint', **private_post())
def post_player_sns_token():
    player_id = get_user_id_from_jwt(bp_notification)
    data = bp_notification.current_request.json_body
    data.update({'player_id': player_id})

    try:
        request = PostPlayerSnsEndpointRequestModel(data)
        interactor = PostPlayerSnsEndpointInteractor(
            request=request,
            player_adapter=get_player_adapter(),
            platform_arn=Settings.ANDROID_PUSH_NOTIFICATION_PLATFORM_ARN,
            aws_region=Settings.AWS_DEFAULT_REGION)
        response = interactor.run()
    except PostPlayerSnsEndpointException as exc:
        return server_error(str(exc))
    return success(response())
