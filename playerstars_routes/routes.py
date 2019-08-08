from chalice import Blueprint
from .auth import cors, cupauth

root = Blueprint(__name__)


@root.route('/',
            methods=['GET', 'POST'],
            cors=cors,
            authorizer=cupauth)
def home():
    return "homezinha"
