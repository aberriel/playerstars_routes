from copy import deepcopy

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


class UserNotFoundToAuthorize(BaseException):
    pass


def check_admin_authorization(user_id):
    user_adapter = PlayerAdapter(
        db_endpoint=Settings.DYNAMODB_URL,
        table_name=Settings.PLAYER_TABLE_NAME)
    user = user_adapter.get_by_id(user_id)
    if not user:
        msg = "User not found"
        raise UserNotFoundToAuthorize(msg)
    if not user.is_admin:
        msg = "User isn't admin. Access denied."
        raise UserNotAdminAuthorized(msg)


def _replace_dot(value):
    return value.replace('.', '_dot_')


def make_fields_dot(params):
    new_params = deepcopy(params) if params else {}

    if 'sort_field' in new_params:
        new_value = _replace_dot(new_params['sort_field'])
        new_params['sort_field'] = new_value

    if 'filter_field' in new_params:
        new_value = _replace_dot(new_params['filter_field'])
        new_params['filter_field'] = new_value

    return new_params
