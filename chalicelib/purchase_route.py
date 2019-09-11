from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_domain import Player, Purchase
from chalicelib.chalice_support import (
    private_get, private_delete, private_put, private_post)
from chalicelib.chalice_support import server_error, redirect
from playerstars_interactors import \
    SaveEntityException, PostPurchaseRequestModel, PostPurchaseInteractor
from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings

bp_purchase = Blueprint(__name__)


def get_adapter():
    return PlayerAdapter(
        Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


# @bp_console.route('/', **private_get())
# def get_all_console():
#     return get_all()
#
#
# @bp_console.route('/{entity_id}', **private_get())
# def get_console_by_id(entity_id):
#     return get_by_id(entity_id)
#

@bp_purchase.route('/', **private_post())
def post_console():
    data = bp_purchase.current_request.json_body
    return post(data)


# @bp_console.route('/{entity_id}', **private_put())
# def put_console(entity_id):
#     data = bp_console.current_request.json_body
#     return put(data)
#
#
# @bp_console.route('/{entity_id}', **private_delete())
# def delete_console(entity_id):
#     return delete(entity_id)


def post(json_data):
    request = PostPurchaseRequestModel(json_data)
    interactor = PostPurchaseInteractor(request, get_adapter(), Settings)
    try:
        response = interactor.run()
    except SaveEntityException as e:
        return server_error(str(e))
    return redirect(response)
