from chalice import Blueprint
from playerstars_adapters import ProductAdapter
from playerstars_domain import Product
from chalicelib.settings import Settings
from .basic_entity_route import BasicEntityRoute
from chalicelib.chalice_support import private_get, private_post


bp_product = Blueprint(__name__)


def get_router():
    adapter = ProductAdapter(
        Settings.PRODUCT_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Product, 'product')


@bp_product.route('/', **private_get())
def get_all_product():
    return get_router().get_all()


@bp_product.route('/', **private_post())
def post_product():
    data = bp_product.current_request.json_body
    return get_router().post(data)
