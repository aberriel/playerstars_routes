from chalice import Blueprint
from playerstars_routes.chalice_support.auth import cors, cupauth
from playerstars_routes.chalice_support import not_found
root = Blueprint(__name__)


@root.route('/',
            methods=['GET', 'POST'],
            cors=cors,
            authorizer=cupauth)
def home():
    return not_found('Página não encontrada no projeto playerstars')
