from unittest.mock import MagicMock, patch
from playerstars_routes import \
    post_user_admin, get_user_admin_by_id, get_all_user_admin, \
    UserAdminChaliceRoute, put_user_admin
from playerstars_interactors import \
    SaveUserAdminException, UpdateUserAdminException

import json
import pytest


def make_post_mock_data():
    payload = """{
        "name": "Anselmo Lira",
        "email": "playerstars@playerstars.com.br"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.PostUserAdminInteractor.run')
def test_post_user_admin(mock):
    result = post_user_admin()
    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.PostUserAdminInteractor.run',
       MagicMock(side_effect=SaveUserAdminException('oops')))
def test_post_user_admin_raises():
    result = post_user_admin()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.GetUserAdminInteractor.run')
def test_get_user_admin(mock):
    result = get_user_admin_by_id('id1')
    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.GetUserAdminInteractor.run',
       return_value=None)
def test_get_user_admin_raises(mock):
    result = get_user_admin_by_id('id1')
    mock.assert_called_once()
    assert result.body['message'] == "User Admin não encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.GetAllUsersAdminsInteractor.run')
def test_get_all_users_admins(mock):
    result = get_all_user_admin()

    mock.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
@patch('playerstars_routes.user_admin_route.GetAllUsersAdminsInteractor.run',
       return_value=None)
def test_get_all_users_admins_raises(mock):
    result = get_all_user_admin()

    mock.assert_called_once()

    assert result.body['message'] == "Nenhum user admin encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


def make_put_mock_data():
    payload = """{
        "name": "Anselmo Lira",
        "email": "playerstars@playerstars.com.br",
        "entity_id": "1212354"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.user_admin_route.PutUserAdminInteractor.run')
def test_put_console(mock):
    result = put_user_admin('1212354')

    mock.assert_called_once()
    assert result.body['data']
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('app.app', make_put_mock_data())
@patch('playerstars_routes.user_admin_route.PutUserAdminInteractor.run',
       MagicMock(side_effect=UpdateUserAdminException('oops')))
def test_put_user_admin_raises():
    result = put_user_admin('1212354')

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def test_not_implemented():
    with pytest.raises(NotImplementedError) as exc:
        UserAdminChaliceRoute().delete_request_model()
    assert str(exc.value) == 'Não implementado no interactor'
    with pytest.raises(NotImplementedError) as exc:
        UserAdminChaliceRoute().delete_interactor()
    assert UserAdminChaliceRoute().delete_not_found() == \
        'Player não encontrado para ser deletado'
