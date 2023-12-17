from chalice import Blueprint
from playerstars_adapters import ProductAdapter
from playerstars_domain import Product
from playerstars_interactors import GetAllProductsInteractor, GetPlanListInteractor

from chalicelib.chalice_support import private_get, private_post
from chalice_support import success, not_found
from chalicelib.settings import Settings
from .basic_entity_route import BasicEntityRoute

bp_product = Blueprint(__name__)
bp_plan = Blueprint(__name__)


def get_router():
    return BasicEntityRoute(get_adapter(), Product, 'product')


def get_adapter():
    return ProductAdapter(Settings.PRODUCT_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_product.route('/', **private_get())
def get_all_product():
    return get_all()


@bp_plan.route('/', **private_get())
def get_all_plan():
    interactor = GetPlanListInteractor()
    response = interactor.run()
    return success(response)


@bp_product.route('/', **private_post())
def post_product():
    data = bp_product.current_request.json_body
    return get_router().post(data)


def get_all():
    interactor = GetAllProductsInteractor(get_adapter())
    response = interactor.run()
    if response:
        return success(response)
    return not_found(f'No product found')
