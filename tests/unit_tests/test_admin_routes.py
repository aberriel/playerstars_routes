from chalicelib.admin_routes import (
    duel_router,
    privacy_router,
    terms_router,

    delete_console_admin,
    delete_privacy_admin,
    delete_terms_admin,
    get_all_consoles_admin,
    get_all_duel_admin,
    get_all_games_admin,
    get_all_players_admin,
    get_all_privacy_admin,
    get_all_terms_admin,
    get_console_by_id_admin,
    get_duel_by_id_admin,
    get_player_by_id_admin,
    get_privacy_by_id_admin,
    get_terms_by_id_admin,
    post_console_admin,
    post_privacy_admin,
    post_terms_admin,
    put_console_admin,
    put_player_admin,
    put_privacy_admin,
    put_terms_admin
)
from chalicelib.utils import UserNotAdminAuthorized
from playerstars_interactors import (
    GetAllGamesAdminException,
    UpdateEntityException)
from unittest.mock import MagicMock, patch
import json


path = 'chalicelib.admin_routes'


@patch('chalicelib.admin_routes.get_all_admin')
@patch('chalicelib.admin_routes.player_router')
def test_get_all_players_admin(mock_player_router, mock_get_all_admin):
    result = get_all_players_admin()
    mock_get_all_admin.assert_called_with(mock_player_router())
    assert result == mock_get_all_admin()


@patch('chalicelib.admin_routes.get_all_admin')
@patch('chalicelib.admin_routes.console_router')
def test_get_all_consoles_admin(mock_console_router, mock_get_all_admin):
    result = get_all_consoles_admin()

    mock_get_all_admin.assert_called_with(mock_console_router())
    assert result == mock_get_all_admin()


def query_params():
    return {
        'pagination_page': 1,
        'pagination_per_page': 10
    }


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin',
       MagicMock(current_request=MagicMock(
           query_params=query_params())))
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       return_value=MagicMock())
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_players_admin_with_queryparam(
        client, resource, run, check, get):
    result = get_all_players_admin()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 206


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin',
       MagicMock(current_request=MagicMock(
           query_params=query_params())))
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       return_value=MagicMock())
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin_with_queryparam(
        client, resource, run, check, get):
    result = get_all_consoles_admin()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 206


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_players_admin_unauthorized(client, resource, cehck, get):
    result = get_all_players_admin()

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_admin_unauthorized(client, resource, cehck, get):
    result = get_all_consoles_admin()

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_by_id_admin(client, resource, run, check, get):
    result = get_player_by_id_admin('12344')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin(client, resource, run, check, get):
    result = get_console_by_id_admin('12344')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


def make_post_mock_data():
    payload = """{
    "name": "Super Nintendo",
    "logo_path": "/images/ss.png",
    "tag_name": "nick#1",
    "games" : []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_post_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_admin(client, resource, run, check, get):
    result = post_console_admin()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


def make_put_mock_data():
    payload = """{
    "entity_id": "id1",
    "name": "Super Nintendo",
    "logo_path": "/images/ss.png",
    "tag_name": "nick#1",
    "games" : []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_put_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console_admin(client, resource, run, check, get):
    result = put_console_admin('12344')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console_admin(client, resource, run, check, get):
    result = delete_console_admin('12344')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_by_id_admin_unauthorized(client, resource, cehck, get):
    result = get_player_by_id_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_post_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_admin_unauthorized(client, resource, run, check, get):
    result = post_console_admin()

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_put_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicPutInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_console_admin_unauthorized(client, resource, run, check, get):
    result = put_console_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicDeleteInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_console_admin_unauthorized(client, resource, run, check, get):
    result = delete_console_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_console_by_id_admin_unauthorized(client, resource, cehck, get):
    result = get_console_by_id_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


def make_put_mock_data():
    return MagicMock(current_request=MagicMock(
        json_body={'entity_id': "1234", "is_admin": True}))


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_put_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.admin_routes.PutPlayerIsAdminInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_player_is_admin(client, resource, run, check, get):
    result = put_player_admin('12344')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_put_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch('chalicelib.admin_routes.PutPlayerIsAdminInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_player_is_admin_unauthorized(client, resource, cehck, get):
    result = put_player_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.bp_admin', make_put_mock_data())
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization',
       side_effect=UpdateEntityException('oops'))
@patch('chalicelib.admin_routes.PutPlayerIsAdminInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_player_is_admin_server_error(client, resource, cehck, get):
    result = put_player_admin('12344')

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 500


@patch('chalicelib.admin_routes.DuelAdapter')
@patch('chalicelib.admin_routes.BasicEntityRoute')
def test_duel_router(routes, adapter):
    router = duel_router()
    assert router


router_mock = MagicMock()


@patch('chalicelib.admin_routes.get_all_admin')
@patch('chalicelib.admin_routes.duel_router', return_value=router_mock)
def test_get_all_duel_admin(router, get_all):
    result = get_all_duel_admin()
    get_all.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.get_by_id_admin')
@patch('chalicelib.admin_routes.duel_router', return_value=router_mock)
def test_get_duel_by_id_admin(router, get_all):
    result = get_duel_by_id_admin('entity_id')
    get_all.assert_called_with('entity_id', router_mock)
    assert result


######################
@patch('chalicelib.admin_routes.TermsAdapter')
@patch('chalicelib.admin_routes.BasicEntityRoute')
def test_terms_router(routes, adapter):
    router = terms_router()
    assert router


@patch('chalicelib.admin_routes.get_all_admin')
@patch('chalicelib.admin_routes.terms_router', return_value=router_mock)
def test_get_all_terms_admin(router, get_all):
    result = get_all_terms_admin()
    get_all.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.get_by_id_admin')
@patch('chalicelib.admin_routes.terms_router', return_value=router_mock)
def test_get_terms_by_id_admin(router, get):
    result = get_terms_by_id_admin('entity_id')
    get.assert_called_with('entity_id', router_mock)
    assert result


@patch('chalicelib.admin_routes.post_admin')
@patch('chalicelib.admin_routes.terms_router', return_value=router_mock)
def test_post_terms_admin(router, post):
    result = post_terms_admin()
    post.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.put_admin')
@patch('chalicelib.admin_routes.terms_router', return_value=router_mock)
def test_put_terms_admin(router, put):
    result = put_terms_admin('entityd_id')
    put.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.delete_admin')
@patch('chalicelib.admin_routes.terms_router', return_value=router_mock)
def test_delete_terms_admin(router, delete):
    result = delete_terms_admin('entity_id')
    delete.assert_called_with('entity_id', router_mock)
    assert result


@patch('chalicelib.admin_routes.PrivacyPolicyAdapter')
@patch('chalicelib.admin_routes.BasicEntityRoute')
def test_privacy_router(routes, adapter):
    router = privacy_router()
    assert router


@patch('chalicelib.admin_routes.get_all_admin')
@patch('chalicelib.admin_routes.privacy_router', return_value=router_mock)
def test_get_all_privacy_admin(router, get_all):
    result = get_all_privacy_admin()
    get_all.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.get_by_id_admin')
@patch('chalicelib.admin_routes.privacy_router', return_value=router_mock)
def test_get_privacy_by_id_admin(router, get):
    result = get_privacy_by_id_admin('entity_id')
    get.assert_called_with('entity_id', router_mock)
    assert result


@patch('chalicelib.admin_routes.post_admin')
@patch('chalicelib.admin_routes.privacy_router', return_value=router_mock)
def test_post_privacy_admin(router, post):
    result = post_privacy_admin()
    post.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.put_admin')
@patch('chalicelib.admin_routes.privacy_router', return_value=router_mock)
def test_put_privacy_admin(router, put):
    result = put_privacy_admin('entityd_id')
    put.assert_called_with(router_mock)
    assert result


@patch('chalicelib.admin_routes.delete_admin')
@patch('chalicelib.admin_routes.privacy_router', return_value=router_mock)
def test_delete_privacy_admin(router, delete):
    result = delete_privacy_admin('entity_id')
    delete.assert_called_with('entity_id', router_mock)
    assert result


# noinspection PyUnusedLocal
@patch(f'{path}.get_user_id_from_jwt')
@patch(f'{path}.console_adapter')
@patch(f'{path}.check_admin_authorization')
@patch(f'{path}.GetAllGamesAdminInteractor')
@patch(f'{path}.success')
@patch(f'{path}.unauthorized')
@patch(f'{path}.server_error')
def test_get_all_games_admin(server_error_mock,
                             unauthorized_mock,
                             success_mock,
                             get_all_interactor_mock,
                             check_admin_mock,
                             console_adapter_mock,
                             get_user_id_from_jwt_mock):
    result = get_all_games_admin()
    get_user_id_from_jwt_mock.assert_called()
    check_admin_mock.assert_called_with(get_user_id_from_jwt_mock())
    console_adapter_mock.assert_called()
    get_all_interactor_mock.assert_called_with(
        console_adapter=console_adapter_mock())
    get_all_interactor_mock().run.assert_called()
    success_mock.assert_called_with(get_all_interactor_mock().run()())
    server_error_mock.assert_not_called()
    unauthorized_mock.assert_not_called()
    assert result == success_mock()


# noinspection PyUnusedLocal
@patch(f'{path}.get_user_id_from_jwt')
@patch(f'{path}.console_adapter')
@patch(f'{path}.check_admin_authorization',
       side_effect=UserNotAdminAuthorized('oops'))
@patch(f'{path}.GetAllGamesAdminInteractor')
@patch(f'{path}.success')
@patch(f'{path}.unauthorized')
@patch(f'{path}.server_error')
def test_get_all_games_admin_user_not_admin_error(server_error_mock,
                                                  unauthorized_mock,
                                                  success_mock,
                                                  get_all_interactor_mock,
                                                  check_admin_mock,
                                                  cosole_adapter_mock,
                                                  get_user_id_from_jwt_mock):
    response = get_all_games_admin()
    get_user_id_from_jwt_mock.assert_called()
    check_admin_mock.assert_called_with(get_user_id_from_jwt_mock())
    get_all_interactor_mock.assert_not_called()
    success_mock.assert_not_called()
    server_error_mock.assert_not_called()
    unauthorized_mock.asert_called_with('oops')
    assert response == unauthorized_mock()


# noinspection PyUnusedLocal
@patch(f'{path}.get_user_id_from_jwt')
@patch(f'{path}.console_adapter')
@patch(f'{path}.check_admin_authorization')
@patch(f'{path}.GetAllGamesAdminInteractor.run',
       side_effect=GetAllGamesAdminException('oops'))
@patch(f'{path}.success')
@patch(f'{path}.unauthorized')
@patch(f'{path}.server_error')
def test_get_all_games_admin_get_all_error(server_error_mock,
                                           unauthorized_mock,
                                           success_mock,
                                           run_mock,
                                           check_admin_mock,
                                           console_adapter_mock,
                                           get_user_id_from_jwt_mock):
    response = get_all_games_admin()
    get_user_id_from_jwt_mock.assert_called()
    check_admin_mock.assert_called_with(get_user_id_from_jwt_mock())
    run_mock.assert_called()
    success_mock.assert_not_called()
    unauthorized_mock.assert_not_called()
    server_error_mock.assert_called_with('oops')
    assert response == server_error_mock()
