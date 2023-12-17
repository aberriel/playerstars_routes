from chalice import Blueprint
from chalice_support import server_error, success
from chalicelib.chalice_support import private_post
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from playerstars_adapters import PlayerAdapter
from playerstars_interactors import (
    PostPurchaseNotificationByGoogleInteractor,
    PostPurchaseNotificationByGoogleRequestModel)

bp_google = Blueprint(__name__)


def get_player_adapter():
    return PlayerAdapter(table_name=Settings.PLAYER_TABLE_NAME, db_endpoint=Settings.DYNAMODB_URL)


@bp_google.route('/', **private_post())
def post_google_purchase_notify():
    data = bp_google.current_request.json_body
    player_id = get_user_id_from_jwt(bp_google)
    data.update({'player_id': player_id})
    return notify_google_purchase(data)


def notify_google_purchase(data):
    try:
        request = PostPurchaseNotificationByGoogleRequestModel(data)
        interactor = PostPurchaseNotificationByGoogleInteractor(request=request, player_adapter=get_player_adapter())
        response = interactor.run()
        return success(response())
    except BaseException as exc:
        return server_error(str(exc))
