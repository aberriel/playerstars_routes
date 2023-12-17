from .wirecard_adapters import (
    get_credit_card_adapter,
    get_plan_adapter,
    get_subscriber_adapter,
    get_subscription_adapter)
from chalice import Blueprint
from chalicelib.aspect.logging import logger_aspect
from chalicelib.chalice_support import private_post
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from chalice_support import created, server_error
from playerstars_adapters import PlayerAdapter
from playerstars_interactors import (
    RedStarsPurchaseInteractor,
    RedStarsPurchaseRequestModel)
from playerstars_interactors.wirecard.red_stars_purchase import \
    RedStarPurchaseInteractorAdapters


bp_wirecard = Blueprint(__name__)


def get_player_adapter():
    return PlayerAdapter(
        table_name=Settings.PLAYER_TABLE_NAME,
        db_endpoint=Settings.DYNAMODB_URL)


def mount_interactor_adapters(customer_id):
    return RedStarPurchaseInteractorAdapters(
        credit_card_adapter=get_credit_card_adapter(customer_id),
        plan_adapter=get_plan_adapter(),
        player_adapter=get_player_adapter(),
        subscriber_adapter=get_subscriber_adapter(),
        subscription_adapter=get_subscription_adapter())


@bp_wirecard.route('/', **private_post())
def post_wirecard_purchase():
    data = bp_wirecard.current_request.json_body
    player_id = get_user_id_from_jwt(bp_wirecard)
    data.update({'code': player_id})
    return purchase_red_stars(json_data=data, player_id=player_id)


@logger_aspect
def purchase_red_stars(json_data, player_id):
    try:
        adapters = mount_interactor_adapters(player_id)
        request = RedStarsPurchaseRequestModel(json_data)
        interactor = RedStarsPurchaseInteractor(adapters=adapters, request=request)
        response = interactor.run()
        return created(response())
    except BaseException as exc:
        return server_error(str(exc))
