from base64 import b64decode

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

    logger.debug("Extracting user name from token: {}".format(authorization_token))

    entity_id_field = 'cognito:username'
    payload = authorization_token.split('.')[1]
    payload = payload + '=' * (len(payload) % 4)
    payload = json.loads(b64decode(payload).decode('utf-8'))
    logger.debug('decoded payload: {}'.format(payload))

    return payload[entity_id_field]


class UserNotAdminAuthorized(BaseException):
    pass
