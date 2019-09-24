from chalice import Blueprint
from chalicelib.chalice_support import (private_post)

from playerstars_interactors.mail import (
    SendMailRequestModel, SendMailInteractor
)
from chalicelib.chalice_support import server_error, success

bp_email = Blueprint(__name__)


@bp_email.route('/send', **private_post())
def post_email():
    data = bp_email.current_request.json_body
    entity_id = get_user_id_from_jwt(bp_email)
    return post(data, entity_id)


<<<<<<< Updated upstream
def post(json_data):
    request = SendMailRequestModel(json_data)
=======
def post(json_data, entity_id):
    response = get_player_by_id(entity_id)
    print(dir(response))
    print(response)
    if response.body['status'] == 'error':
        raise BaseException('Player não encontrado')
    request = SendMailRequestModel(json_data, response.body)
>>>>>>> Stashed changes
    interactor = SendMailInteractor(request)
    try:
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)



