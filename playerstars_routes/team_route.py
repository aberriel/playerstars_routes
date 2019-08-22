#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import cors, cupauth
from chalice import Blueprint
from playerstars_interactors import (
    ConsoleModel,
    GameModel,
    GetAllTeamsInteractor,
    GetAllTeamsResponseModel,
    GetTeamByUserInteractor,
    GetTeamByUserRequestModel,
    GetTeamByUserResponseModel,
    GetTeamInteractor,
    GetTeamRequestModel,
    GetTeamResponseModel,
    MembershipType,
    PostTeamInteractor,
    PostTeamRequestModel,
    PostTeamResponseModel,
    PutTeamInteractor,
    PutTeamRequestModel,
    PutTeamResponseModel,
    SaveTeamException,
    UpdateTeamException
)
from playerstars_routes.basic_route import BasicRoute
from playerstars_routes.chalice_support import (
    success,
    not_found, server_error, created
)

bp_console = Blueprint(__name__)


@bp_console.route('/team', methods=['GET'], cors=cors, authorizer=cupauth)
def get_all_teams():
    return TeamRoute().get_all()


@bp_console.route('/team/{entity_id}',
                  methods=['GET'],
                  cors=cors, authorizer=cupauth)
def get_team_by_id(entity_id):
    return TeamRoute().get_by_id(entity_id)


@bp_console.route('/team/byuser/{user_id}',
                  methods=['GET'],
                  cors=cors, authorizer=cupauth)
def get_all_teams_by_user(user_id):
    return TeamRoute().get_by_user(user_id)


@bp_console.route('/team',
                  methods=['POST'],
                  cors=cors,
                  authorizer=cupauth)
def post_team():
    from app import app
    data = app.current_request.json_body
    return TeamRoute().post(data)


@bp_console.route('/team/{entity_id}',
                  methods=['PUT'],
                  cors=cors,
                  authorizer=cupauth)
def put_team(entity_id):
    from app import app
    data = app.current_request.json_body
    return TeamRoute().put(data)


class TeamRoute(BasicRoute):
    def make_game_model(self, game_list_data):
        game_model_list = list()
        for game_data in game_list_data:
            game_model = GameModel(game_id=game_data['game_id'],
                                   name=game_data['name'],
                                   logo_path=game_data['logo_path'])
            game_model_list.append(game_model)
        return game_model_list

    def make_console_model(self, console_list_data):
        console_model_list = list()
        for console_data in console_list_data:
            game_model_list = self.make_game_model(console_data['games'])
            console_model = ConsoleModel(console_id=console_data['console_id'],
                                         name=console_data['name'],
                                         logo_path=console_data['logo_path'],
                                         games=game_model_list)
            console_model_list.append(console_model)
        return console_model_list

    def make_post_request(self, data):
        console_list = self.make_console_model(data['consoles'])
        game_list = self.make_game_model(data['games'])
        request_data = PostTeamRequestModel(name=data['name'],
                                            captain=data['captain'],
                                            consoles=console_list,
                                            games=game_list,
                                            members=data['members'])
        return request_data

    def make_put_request(self, data):
        console_list = self.make_console_model(data['consoles'])
        game_list = self.make_game_model(data['games'])
        request_data = PutTeamRequestModel(team_id=data['team_id'],
                                           name=data['name'],
                                           captain=data['captain'],
                                           consoles=console_list,
                                           games=game_list,
                                           members=data['members'])
        return request_data

    def get_by_user(self, player_id):
        request = GetTeamByUserRequestModel(membership_type=MembershipType.ALL,
                                            player_id=player_id)
        interactor = GetTeamByUserInteractor(request)
        response = interactor.run()
        if response:
            return success(response)
        return not_found(self.not_found_message())

    def not_found_message(self):
        return 'Time não encontrado'

    def not_found_all_message(self):
        return 'Nenhum console encontrado'

    def get_all_interactor(self):
        return GetAllTeamsInteractor

    def get_interactor(self):
        return GetTeamInteractor

    def get_request_model(self):
        return GetTeamRequestModel

    def post_interactor(self):
        return PostTeamInteractor

    def save_exception(self):
        return SaveTeamException

    def put_interactor(self):
        return PutTeamInteractor

    def update_exception(self):
        return UpdateTeamException

    def delete_interactor(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_not_found(self):
        raise NotImplementedError('Não implementado no interactor')

    def delete_request_model(self):
        raise NotImplementedError('Não implementado no interactor')
