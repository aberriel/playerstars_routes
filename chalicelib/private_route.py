from chalice_support.private_blueprint import PrivateBlueprint
from chalicelib.playerstars_auth import cors, authorizer


class PrivateRoute(PrivateBlueprint):
    def __init__(self, name):
        super().__init__(name, cors, authorizer)
