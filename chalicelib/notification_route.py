from chalice import Blueprint
from playerstars_adapters import (
    NotificationAdapter)
from chalicelib.settings import Settings
from playerstars_domain import Notification
from chalicelib.chalice_support import private_post
from playerstars_interactors import \
    PostAppNotificationInteractor, BasicPostRequestModel, SaveEntityException
from chalicelib.chalice_support import (
    server_error, created)

bp_notification = Blueprint(__name__)


def get_notification_adapter():
    return NotificationAdapter(
        Settings.NOTIFICATION_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_notification.route('/', **private_post())
def post_app_notification():
    data = bp_notification.current_request.json_body
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
