from chalice import Blueprint
from playerstars_adapters import NotificationAdapter
from playerstars_domain import Notification
from playerstars_interactors import (
    BasicPostRequestModel, GetAppNotificationByUserInteractor,
    GetAppNotificationByUserRequestModel, PostAppNotificationInteractor,
    PostNotificationReadInteractor, PostNotificationReadException,
    PostNotificationReadRequestModel, SaveEntityException
)
from chalicelib.chalice_support import private_post, private_get
from chalice_support import (server_error, created, success, not_found)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

bp_notification = Blueprint(__name__)


def get_notification_adapter():
    return NotificationAdapter(Settings.NOTIFICATION_TABLE_NAME,
                               Settings.DYNAMODB_URL)


@bp_notification.route('/', **private_post())
def post_app_notification():
    data = bp_notification.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_notification)
    data.update({'player_id': entity_id})
    return post(data)


def post(json_data):
    adapter = get_notification_adapter()
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
    notification_adapter = get_notification_adapter()
    request = GetAppNotificationByUserRequestModel(entity_id, status)
    interactor = GetAppNotificationByUserInteractor(
        request=request,
        adapter_instance=notification_adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'No notifications found for player id:'
                     f' {entity_id}')


@bp_notification.route('/read/{entity_id}', **private_post())
def post_notification_as_read(entity_id):
    try:
        player_id = get_user_id_from_jwt(bp_notification)
        adapter = get_notification_adapter()
        request = PostNotificationReadRequestModel(player_id, entity_id)
        interactor = PostNotificationReadInteractor(request, adapter)
        response = interactor.run()
    except PostNotificationReadException as e:
        return server_error(str(e))
    return success(response)
