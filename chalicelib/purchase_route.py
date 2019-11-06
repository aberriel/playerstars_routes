from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_domain import Player
from chalicelib.chalice_support import (
    private_get, private_post, private_delete)
from chalicelib.chalice_support.auth import cors
from chalicelib.basic_entity_route import BasicEntityRoute
from chalicelib.settings import Settings

from chalicelib.utils import get_user_id_from_jwt

from playerstars_interactors import (
    PostPurchaseException,
    PostPurchaseInteractor,
    PostPurchaseRequestModel,

    PostNotificationInteractor,
    PostNotificationRequestModel,
    PagSeguroException,

    GetPurchaseHistoryInteractor,
    GetPurchaseHistoryRequestModel
)

from chalicelib.chalice_support import (
    server_error, created, success, not_found)

bp_purchase = Blueprint(__name__)


def get_adapter():
    return PlayerAdapter(
        Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_purchase.route('/', **private_post())
def post_purchase():
    data = bp_purchase.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_purchase)
    data.update({'entity_id': entity_id})
    return post(data)


def post(json_data):
    adapter = get_adapter()
    request = PostPurchaseRequestModel(json_data)
    interactor = PostPurchaseInteractor(
        request=request,
        player_id=json_data['entity_id'],
        adapter_class=adapter,
        settings=Settings)
    try:
        response = interactor.run()
    except PostPurchaseException as e:
        return server_error(str(e))
    return created(response)


@bp_purchase.route('/notification', methods=['POST'],
                   content_types=['application/x-www-form-urlencoded'],
                   cors=cors)
def post_notification():
    adapter = get_adapter()
    data = bp_purchase.current_request.raw_body
    request = PostNotificationRequestModel(data)
    interactor = PostNotificationInteractor(request, Settings, adapter)
    try:
        response = interactor.run()
    except PagSeguroException as e:
        return server_error(str(e))
    return success(response)


@bp_purchase.route('/history/', **private_get())
def get_history_route():
    entity_id = get_user_id_from_jwt(bp_purchase)
    return get_history({'player_id': entity_id})


def get_history(data):
    adapter = get_adapter()
    request = GetPurchaseHistoryRequestModel(data)
    interactor = GetPurchaseHistoryInteractor(request, adapter)
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'Histórico de compras do player {data["player_id"]}'
                     f' não encontrado')
