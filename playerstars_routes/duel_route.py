#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import GetMatchListRequestModel, \
    GetMatchListInteractor, CreateDuelException, CreateDuelInteractor, \
    CreateDuelRequestModel
from playerstars_routes.basic_route import BasicRoute

bp_match = Blueprint(__name__)


@bp_match.route(
    '/match-list/{user_id}', methods=['GET'], cors=cors, authorizer=cupauth)
def get_match_list(user_id):
    return MatchListRoute().get_by_id(user_id)


@bp_match.route(
    '/match-send/', methods=['POST'], cors=cors, authorizer=cupauth)
def post_match():
    from app import app
    data = app.current_request.json_body
    return MatchListRoute().post(data)


class MatchListRoute(BasicRoute):

    def make_post_request(self, data):
        return CreateDuelRequestModel(
            player_id=data['player_id'])

    def make_put_request(self, data):
        raise NotImplementedError('Não implementado')

    def get_all_interactor(self):
        raise NotImplementedError('Não implementado')

    def not_found_message(self):
        return 'Nenhum match encontrado'

    def not_found_all_message(self):
        return 'Não implementado'

    def get_request_model(self):
        return GetMatchListRequestModel

    def get_interactor(self):
        return GetMatchListInteractor

    def save_exception(self):
        return CreateDuelException

    def post_interactor(self):
        return CreateDuelInteractor

    def update_exception(self):
        raise NotImplementedError('Não implementado')

    def put_interactor(self):
        raise NotImplementedError('Não implementado')

    def delete_request_model(self):
        raise NotImplementedError('Não implementado')

    def delete_interactor(self):
        raise NotImplementedError('Não implementado')

    def delete_not_found(self):
        raise NotImplementedError('Não implementado')
