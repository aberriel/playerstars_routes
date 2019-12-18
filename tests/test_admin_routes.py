from chalicelib import get_all_players_admin
from chalicelib.utils import UserNotAdminAuthorized
from unittest.mock import MagicMock, patch


# noinspection PyUnusedLocal
@patch('chalicelib.admin_routes.get_user_id_from_jwt')
@patch('chalicelib.admin_routes.check_admin_authorization')
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_players_admin(client, resource, run, check, get):
    result = get_all_players_admin()
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
def test_get_all_players_admin_unauthorized(client, resource, cehck, get):
    result = get_all_players_admin()

    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"
    assert result.status_code == 401
