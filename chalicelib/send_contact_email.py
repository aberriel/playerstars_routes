from chalice import Blueprint
from chalicelib.chalice_support import (
    private_post,
    server_error,
    success
)
from chalicelib.player_route import get_player_by_id
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from playerstars_adapters import PlayerAdapter
from playerstars_interactors.send_mail import (
    SendContactMailInteractor,
    SendContactMailRequestModel
)


bp_contact_email = Blueprint(__name__)


@bp_contact_email.route('/send', **private_post())
def post_contact_email():
    data = bp_contact_email.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_contact_email)
    return post(data, entity_id)


def post(json_data, entity_id):
    adapter = PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
    request = SendContactMailRequestModel(json_data, entity_id)
    interactor = SendContactMailInteractor(request, adapter)
    try:
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)
