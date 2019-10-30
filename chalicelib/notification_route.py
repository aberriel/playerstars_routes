from chalice import Blueprint
from playerstars_adapters import (
    NotificationAdapter)
from chalicelib.settings import Settings
from playerstars_domain import Notification
from chalicelib.chalice_support import private_post, private_get
from playerstars_interactors import (
    PostAppNotificationInteractor, BasicPostRequestModel, SaveEntityException,
    GetAppNotificationByUserInteractor, GetAppNotificationByUserRequestModel)
from chalicelib.chalice_support import (
    server_error, created, success, not_found)
from chalicelib.utils import get_user_id_from_jwt

bp_notification = Blueprint(__name__)


def get_notification_adapter():
    return NotificationAdapter(
        Settings.NOTIFICATION_TABLE_NAME, Settings.DYNAMODB_URL)


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
    return get_by_user(entity_id)


def get_by_user(entity_id):
    adapter = get_notification_adapter()
    request = GetAppNotificationByUserRequestModel(entity_id)
    interactor = GetAppNotificationByUserInteractor(request, adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Nenhuma notificação encontrada para o player id:'
                     f' {entity_id}')
