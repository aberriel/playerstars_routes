# from chalice import Blueprint
# from chalicelib.chalice_support import (private_get, private_post)
# from chalice_support import (not_found, server_error, success, created)
# from chalicelib.settings import Settings
# from chalicelib.utils import get_user_id_from_jwt
# from playerstars_adapters import (
#     ChampionshipAdapter,
#     DuelAdapter,
#     PlayerAdapter,
#     TeamAdapter,)
# from playerstars_graphql_adapters import NotificationAdapter
# from playerstars_interactors import (
#     AcceptInvitationException,
#     AcceptInvitationInteractor,
#     AcceptInvitationRequestModel,
#
#     AddFriendToChampionshipException,
#     AddFriendToChampionshipInteractor,
#     AddFriendToChampionshipRequestModel,
#
#     CreateChampionshipException,
#     CreateChampionshipRequestModel,
#     CreateChampionshipInteractor,
#
#     GetAllChampionshipsInteractor,
#     GetChampionshipInteractor,
#     GetChampionshipRequestModel,
#     GetChampionshipsByMemberInteractor,
#     GetChampionshipsByMemberRequestModel,
#     GetOpenChampionshipsByTypeInteractor,
#     GetOpenChampionshipsByTypeRequestModel,
#
#     JoinOpenChampionshipException,
#     JoinOpenChampionshipInteractor,
#     JoinOpenChampionshipRequestModel
# )
#
#
# bp_accept_invitation = Blueprint(__name__)
# bp_add_friend_to_championship = Blueprint(__name__)
# bp_championship = Blueprint(__name__)
# bp_join_open_championship = Blueprint(__name__)
#
#
# def get_championship_adapter():
#     return ChampionshipAdapter(Settings.CHAMPIONSHIP_TABLE_NAME,
#                                Settings.DYNAMODB_URL)
#
#
# def get_duel_adapter():
#     return DuelAdapter(Settings.DUEL_TABLE_NAME,
#                        Settings.DYNAMODB_URL)
#
#
# def get_player_adapter():
#     return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)
#
#
# def get_team_adapter():
#     return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)
#
#
# def get_notification_adapter():
#     return NotificationAdapter(
#         api_id=Settings.GRAPHQL_API_ID,
#         api_key=Settings.GRAPHQL_API_KEY,
#         aws_region=Settings.AWS_DEFAULT_REGION)
#
#
# @bp_championship.route('/', **private_get())
# def get_all_championships():
#     try:
#         interactor = GetAllChampionshipsInteractor(
#             championship_adapter=get_championship_adapter(),
#             duel_adapter=get_duel_adapter(),
#             player_adapter=get_player_adapter(),
#             team_adapter=get_team_adapter())
#         response = interactor.run()
#         if response:
#             return success(response)
#         return not_found('No championship found')
#     except BaseException as exc:
#         return server_error(str(exc))
#
#
# @bp_championship.route('/{championship_id}', **private_get())
# def get_championship_by_id(championship_id):
#     try:
#         request = GetChampionshipRequestModel(championship_id)
#         interactor = GetChampionshipInteractor(
#             request=request,
#             championship_adapter=get_championship_adapter(),
#             duel_adapter=get_duel_adapter(),
#             player_adapter=get_player_adapter(),
#             team_adapter=get_team_adapter())
#         response = interactor.run()
#
#         if response:
#             return success(response)
#         return not_found('Championship not found')
#     except BaseException as exc:
#         return server_error(str(exc))
#
#
# @bp_championship.route('/find-by-player', **private_get())
# def get_championships_by_player():
#     player_id = get_user_id_from_jwt(bp_championship)
#     try:
#         request = GetChampionshipsByMemberRequestModel(player_id, 'Player')
#         interactor = GetChampionshipsByMemberInteractor(
#             request=request,
#             championship_adapter=get_championship_adapter(),
#             duel_adapter=get_duel_adapter(),
#             player_adapter=get_player_adapter(),
#             team_adapter=get_team_adapter())
#         response = interactor.run()
#
#         if response:
#             return success(response)
#         return not_found('No championship found')
#     except BaseException as exc:
#         return server_error(str(exc))
#
#
# @bp_championship.route('/find-by-team/{team_id}', **private_get())
# def get_championships_by_team(team_id):
#     try:
#         request = GetChampionshipsByMemberRequestModel(team_id, 'Player')
#         interactor = GetChampionshipsByMemberInteractor(
#             request=request,
#             championship_adapter=get_championship_adapter(),
#             duel_adapter=get_duel_adapter(),
#             player_adapter=get_player_adapter(),
#             team_adapter=get_team_adapter())
#         response = interactor.run()
#
#         if response:
#             return success(response)
#         return not_found('No championship found')
#     except BaseException as exc:
#         return server_error(str(exc))
#
#
# @bp_championship.route('/find-open/{championship_type}', **private_get())
# def get_open_championships(championship_type):
#     championship_adapter = get_championship_adapter()
#     duel_adapter = get_duel_adapter()
#     player_adapter = get_player_adapter()
#     team_adapter = get_team_adapter()
#
#     try:
#         request = GetOpenChampionshipsByTypeRequestModel(championship_type)
#         interactor = GetOpenChampionshipsByTypeInteractor(
#             request=request,
#             championship_adapter=championship_adapter,
#             duel_adapter=duel_adapter,
#             player_adapter=player_adapter,
#             team_adapter=team_adapter)
#         response = interactor.run()
#
#         if response:
#             return success(response)
#         return not_found('No championship found')
#     except BaseException as exc:
#         return server_error(str(exc))
#
#
# @bp_championship.route('/', **private_post())
# def post_create_championship():
#     data = bp_championship.current_request.json_body
#     entity_id = get_user_id_from_jwt(bp_championship)
#     if not data.get('owner', None):
#         data.update({'owner': entity_id})
#
#     request = CreateChampionshipRequestModel(data)
#     interactor = CreateChampionshipInteractor(
#         request=request,
#         championship_adapter=get_championship_adapter(),
#         player_adapter=get_player_adapter(),
#         team_adapter=get_team_adapter(),
#         notification_adapter=get_notification_adapter()
#     )
#
#     try:
#         response = interactor.run()
#     except CreateChampionshipException as exc:
#         return server_error(str(exc))
#     return created(response())
#
#
# @bp_championship.route('/accept-invitation', **private_post())
# def post_accept_invitation():
#     data = bp_championship.current_request.json_body
#     entity_id = get_user_id_from_jwt(bp_championship)
#     data.update({'entity_id': entity_id})
#
#     request = AcceptInvitationRequestModel(
#         invitation_code=data['invitation_code'],
#         accepted=data['accepted']
#     )
#     interactor = AcceptInvitationInteractor(
#         request=request,
#         player_adapter=get_player_adapter(),
#         team_adapter=get_team_adapter(),
#         championship_adapter=get_championship_adapter()
#     )
#
#     try:
#         response = interactor.run()
#     except AcceptInvitationException as exc:
#         return server_error(str(exc))
#
#     return success(response)
#
#
# @bp_championship.route('/join', **private_post())
# def post_join_open_championship():
#     data = bp_championship.current_request.json_body
#     entity_id = get_user_id_from_jwt(bp_championship)
#     data.update({'member_id': entity_id})
#
#     request = JoinOpenChampionshipRequestModel(data)
#     interactor = JoinOpenChampionshipInteractor(
#         request=request,
#         championship_adapter=get_championship_adapter(),
#         player_adapter=get_player_adapter(),
#         team_adapter=get_team_adapter())
#
#     try:
#         response = interactor.run()
#     except JoinOpenChampionshipException as exc:
#         return server_error(str(exc))
#
#     return success(response)
#
#
# @bp_championship.route('/add-friend', **private_post())
# def post_add_friend_to_championship():
#     data = bp_championship.current_request.json_body
#     player_id = get_user_id_from_jwt(bp_championship)
#     data.update({'entity_id': player_id})
#
#     request = AddFriendToChampionshipRequestModel(data)
#     interactor = AddFriendToChampionshipInteractor(
#         request=request,
#         championship_adapter=get_championship_adapter(),
#         player_adapter=get_player_adapter(),
#         team_adapter=get_team_adapter(),
#         notification_adapter=get_notification_adapter()
#     )
#
#     try:
#         response = interactor.run()
#     except AddFriendToChampionshipException as exc:
#         return server_error(str(exc))
#
#     return success(response)
