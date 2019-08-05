#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors.player.player_registration import \
    PlayerRegistrationConsoleModel, \
    PlayerRegistrationRequestModel, PlayerRegistrationInteractor, \
    PlayerRegistrationException
from playerstars_routes.chalice_support import (
    server_error, created)


root = Blueprint(__name__)


@root.route('/player/',
            methods=['POST'],
            cors=cors,
            authorizer = cupauth)
def player_registration():
    from app import app
    data = app.current_request.json_body

    # Mounting console data
    raw_consoles = data['consoles']
    consoles = list()
    for raw_console in raw_consoles:
        console = PlayerRegistrationConsoleModel(
            name=raw_console['name'],
            nickname=raw_console['nickname'],
            logo_path=raw_console['logo_path']
        )
        consoles.append(console)

    # Mounting player data
    request = PlayerRegistrationRequestModel(
        name=data['name'],
        nickname=data['nickname'],
        birth_date=data['birth_date'],
        cpf=data['cpf'],
        email=data['email'],
        phone_number=data['phone_number'],
        street=data['street'],
        street_number=data['street_number'],
        street_complement=data['street_complement'],
        neighborhood=data['neighborhood'],
        city=data['city'],
        state=data['state'],
        country=data['country'],
        postal_code=data['postal_code'],
        promo_code=data['promo_code'],
        consoles=consoles,
        profile_image=data['profile_image']
    )

    interactor = PlayerRegistrationInteractor(request)
    try:
        response = interactor.run()
    except PlayerRegistrationException as e:
        return server_error(str(e))
    return created(response)
