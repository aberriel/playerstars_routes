from chalice import Blueprint
from .auth import cors, cupauth

root = Blueprint(__name__)


@root.route('/',
            methods=['GET', 'POST'],
            cors=cors)
def home():
    return "homezinha"
