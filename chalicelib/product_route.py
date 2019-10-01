from chalice import Blueprint
from playerstars_adapters import ProductAdapter
from chalicelib.settings import Settings
from .basic_entity_route import BasicEntityRoute
from chalicelib.chalice_support import private_get


bp_product = Blueprint(__name__)


def get_router():
    adapter = ProductAdapter(
        Settings.PRODUCT_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, ProductAdapter, 'product')


@bp_product.route('/', **private_get())
def get_all_product():
    return get_router().get_all()
