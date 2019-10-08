import json
import logging
from base64 import b64decode
from playerstars_interactors import BasicGetInteractor, BasicGetRequestModel

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
        logger.debug('Não foi localizado Token.')
        raise TokenNotFoundException("Token não encontrado no JWT")

    logger.debug("Extraindo o nome do token: {}".format(authorization_token))

    entity_id_field = 'cognito:username'
    payload = authorization_token.split('.')[1]
    payload = payload + '=' * (len(payload) % 4)
    payload = json.loads(b64decode(payload).decode('utf-8'))
    logger.debug('payload decodificado: {}'.format(payload))

    return payload[entity_id_field]


class UserNotAdminAuthorized(BaseException):
    pass


# def check_admin_authorization(blueprint):
#
#     user_id = get_user_id_from_jwt(blueprint)
#
#     request = BasicGetRequestModel(user_id)
#     interactor = BasicGetInteractor(request)
#     user = interactor.run()
#
#     if not user["is_admin"]:
#         msg = "Usuário não autorizado como admin"
#         raise UserNotAdminAuthorized(msg)
