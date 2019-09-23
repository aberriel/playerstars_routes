from chalice import Blueprint
from chalicelib.chalice_support import (private_post)

from playerstars_interactors.mail import (
    SendMailRequestModel, SendMailInteractor
)
from chalicelib.chalice_support import server_error, success

bp_email = Blueprint(__name__)


@bp_email.route('/send', **private_post())
def post_player():
    data = bp_email.current_request.json_body
    return post(data)


def post(json_data):
    request = SendMailRequestModel(json_data)
    interactor = SendMailInteractor(request)
    try:
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)



