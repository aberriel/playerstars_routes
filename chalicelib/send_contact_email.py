from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_interactors.send_mail import (
    SendContactMailInteractor,
    SendContactMailRequestModel
)

from chalicelib.chalice_support import private_post
from chalice_support import (server_error, success)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

bp_contact_email = Blueprint(__name__)


def get_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_contact_email.route('/send', **private_post())
def post_contact_email():
    data = bp_contact_email.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_contact_email)
    return post(data, entity_id)


def post(json_data, player_id):
    request = SendContactMailRequestModel(json_data, player_id,
                                          Settings.CONTACT_EMAIL_RECIPIENTS)
    interactor = SendContactMailInteractor(request, get_adapter())
    try:
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)
