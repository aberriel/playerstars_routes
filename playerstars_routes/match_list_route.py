#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import GetMatchListRequestModel, \
    GetMatchListInteractor
from playerstars_routes.chalice_support import success, not_found

bp_match = Blueprint(__name__)


@bp_match.route(
    '/match-list/{user_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_match_list(user_id):
    return MatchListRoute().match_list(user_id)


class MatchListRoute:
    def match_list(self, user_id):
        request = GetMatchListRequestModel(user_id)
        interactor = GetMatchListInteractor(request)
        response = interactor.run()
        if response:
            return success(response)
        return not_found('Nenhum match encontrado')
