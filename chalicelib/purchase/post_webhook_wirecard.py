from chalice import Blueprint
from chalice_support import server_error, success
from playerstars_interactors import ReceiveWebhookInteractor

from chalicelib.aspect.logging import logger_aspect
from chalicelib.chalice_support import private_post
from chalicelib.purchase.wirecard_adapters import get_subscription_adapter, get_plan_adapter
from chalicelib.settings import Settings
from playerstars_adapters import PlayerAdapter
from playerstars_interactors.wirecard import WebhookProcessorAdapters


bp_webhook_wirecard = Blueprint(__name__)


def get_player_adapter():
    return PlayerAdapter(
        table_name=Settings.PLAYER_TABLE_NAME,
        db_endpoint=Settings.DYNAMODB_URL)


def mount_webhook_adapters():
    return WebhookProcessorAdapters(
        player_adapter=get_player_adapter(),
        subscription_adapter=get_subscription_adapter(),
        plan_adapter=get_plan_adapter())


@bp_webhook_wirecard.route('/', **private_post())
def post_webhook_wirecard():
    data = bp_webhook_wirecard.current_request.json_body
    return process_received_webhook(data)


@logger_aspect
def process_received_webhook(webhook_data):
    try:
        adapters = mount_webhook_adapters()
        interactor = ReceiveWebhookInteractor(
            webhook_json=webhook_data,
            adapters=adapters)
        response = interactor.run()
        return success(response())
    except BaseException as exc:
        return server_error(str(exc))
