from playerstars_adapters import PlayerAdapter
from base64 import b64decode
from chalicelib.settings import Settings
import json
import logging


logger = logging.getLogger()


class TokenNotFoundException(BaseException):
    pass


def get_authorization_token(blueprint):
    for k, v in blueprint.current_request.headers.items():
        if k.upper() == 'AUTHORIZATION':
            return v
    return None


def get_user_id_from_jwt(blueprint):
    authorization_token = get_authorization_token(blueprint)

    if authorization_token is None:
        logger.debug('Token not found.')
        raise TokenNotFoundException("Token not found on JWT")

    logger.debug(
        "Extracting user name from token: {}".format(authorization_token))

    entity_id_field = 'cognito:username'
    payload = authorization_token.split('.')[1]
    payload = payload + '=' * (len(payload) % 4)
    payload = json.loads(b64decode(payload).decode('utf-8'))
    logger.debug('decoded payload: {}'.format(payload))

    return payload[entity_id_field]


class UserNotAdminAuthorized(BaseException):
    pass


def check_admin_authorization(user_id):
    user_adapter = PlayerAdapter(
        db_endpoint=Settings.DYNAMODB_URL,
        table_name=Settings.PLAYER_TABLE_NAME)
    user = user_adapter.get_by_id(user_id)
    if not user.is_admin:
        msg = "Usuário não autorizado como admin"
        raise UserNotAdminAuthorized(msg)
