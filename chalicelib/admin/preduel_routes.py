from chalice import Blueprint
from chalice_support.basic_routes import BasicChaliceRoutes
from clapy_basic_classes.basic_routes import BasicEntityRoutes
from playerstars_adapters import PreDuelAdapter
from playerstars_domain import PreDuel

from chalicelib.settings import Settings
from chalicelib.playerstars_auth import authorizer, cors


def get_preduel_adatper():
    return PreDuelAdapter(Settings.PREDUEL_TABLE_NAME, Settings.DYNAMODB_URL)


def get_preduel_admin_routes():
    bp_preduel_admin = Blueprint(__name__)
    ber = BasicEntityRoutes(get_preduel_adatper, PreDuel)
    bcr = BasicChaliceRoutes(ber, PreDuel)
    bcr.register_routes(bp_preduel_admin, cors, authorizer)

    return bp_preduel_admin
