from chalice import Blueprint
from playerstars_adapters import PlayerAdapter
from playerstars_interactors.send_mail import (
    SendContactMailInteractor,
    SendContactMailRequestModel,
    SendInvitationMailInteractor,
    SendInvitationMailRequestModel,
    SendWelcomeMailInteractor,
    SendWelcomeMailRequestModel
)

from chalicelib.chalice_support import private_post
from chalice_support import (server_error, success)
from chalicelib.settings import Settings
from chalicelib.utils import get_user_id_from_jwt
from chalicelib.chalice_support.auth import cors
bp_welcome_email = Blueprint(__name__)
bp_invitation_email = Blueprint(__name__)
bp_contact_email = Blueprint(__name__)


def get_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


@bp_contact_email.route('/send', **private_post())
def post_contact_email():
    try:
        data = bp_contact_email.current_request.json_body
        player_id = get_user_id_from_jwt(bp_contact_email)
        request = SendContactMailRequestModel(
            data, Settings.CONTACT_EMAIL_RECIPIENTS, player_id)
        interactor = SendContactMailInteractor(request, get_adapter())
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)


@bp_contact_email.route('/public/send', methods=['POST'], cors=cors)
def post_public_contact_email():
    try:
        data = bp_contact_email.current_request.json_body
        request = SendContactMailRequestModel(
            data, Settings.CONTACT_EMAIL_RECIPIENTS)
        interactor = SendContactMailInteractor(request, get_adapter())
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)


@bp_invitation_email.route('/send', **private_post())
def post_invitation_email():
    try:
        data = bp_invitation_email.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_invitation_email)
        adapter = PlayerAdapter(
            Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
        request = SendInvitationMailRequestModel(data, entity_id)
        interactor = SendInvitationMailInteractor(
            request, adapter, Settings.CONTACT_EMAIL_RECIPIENTS)
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)


@bp_welcome_email.route('/send', **private_post())
def post_welcome_email():
    try:
        data = bp_welcome_email.current_request.json_body
        entity_id = get_user_id_from_jwt(bp_welcome_email)
        adapter = PlayerAdapter(
            Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
        request = SendWelcomeMailRequestModel(data, entity_id)
        interactor = SendWelcomeMailInteractor(request, adapter)
        response = interactor.run()
    except BaseException as e:
        return server_error(str(e))
    return success(response)
