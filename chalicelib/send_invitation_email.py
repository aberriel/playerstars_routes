from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_interactors.send_mail import (
    SendInvitationMailInteractor,
    SendInvitationMailRequestModel
)

from chalicelib.chalice_support import private_post
from chalice_support import (server_error, success)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt

bp_invitation_email = Blueprint(__name__)


@bp_invitation_email.route('/send', **private_post())
def post_invitation_email():
    data = bp_invitation_email.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_invitation_email)
    return post(data, entity_id)


def post(json_data, entity_id):
    adapter = PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    request = SendInvitationMailRequestModel(json_data, entity_id)
    interactor = SendInvitationMailInteractor(
        request, adapter, Settings.CONTACT_EMAIL_RECIPIENTS)
    try:
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)
