from playerstars_interactors import \
    SaveEntityException, SaveFriendsException, UpdateEntityException, \
    AcceptTeamInvitationException, SaveConvertedStarsException
from chalicelib.player_route import (
    get_all_player, get_player_by_id, post_player, get_my_profile,
    get_friends_route, post_friend_route, delete_friend_route,
    put_player, get_all_teams_from_player, post_console_data_route,
    post_accept_terms_route, accept_team_invitation_route,
    convert_star_route, post_friend_route_v2, get_friends_route_v2,
    delete_friend_route_v2, get_ranking_route, get_player_consoles,
    get_friends_by_console_game_route, get_accepted_teams_from_player
)
import json
import pytest
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch
from chalicelib.utils import TokenNotFoundException
from playerstars_adapters import PlayerAdapter


def make_post_mock_data():
    payload = """{
        "user":{
            "name": "Anselmo Lira",
            "email": "playerstars@playerstars.com.br",
            "birth_date": "16/12/1986",
            "street": "Rua José de Figueiredo",
            "street_number": "192",
            "street_complement": "Blocos 29, 30",
            "neighborhood": "Barra da Tijuca",
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "country": "Brasil",
            "postal_code": "22333-000",
            "phone_number": "(21) 99663-6963",
            "cpf": "123.456.789-00",
            "nickname": "anselmo.lira",
            "profile_image": "ACCBB4762CF23AA35690CC"
        },
        "promo_code": "ABC123",
        "favorites": [],
        "red_star_balance": 123,
        "golden_star_balance": 4321,
        "consoles": [
            {
                "entity_id": "1",
                "name": "PS 4",
                "logo_path": "/images/ps4.png",
                "tag_name": "007"
            },
            {
                "entity_id": "11",
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "tag_name": "mario",
                "games": []
            }
        ],
        "states_regions": [],
        "countries_regions": []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player(client, resource, run):
    result = post_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player_raises(client, resource):
    result = post_player()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_put_mock_data():
    payload = """{
        "user":{
            "name": "Anselmo Lira",
            "email": "playerstars@playerstars.com.br",
            "birth_date": "16/12/1986",
            "street": "Rua José de Figueiredo",
            "street_number": "192",
            "street_complement": "Blocos 29, 30",
            "neighborhood": "Barra da Tijuca",
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "country": "Brasil",
            "postal_code": "22333-000",
            "phone_number": "(21) 99663-6963",
            "cpf": "123.456.789-00",
            "nickname": "anselmo.lira",
            "profile_image": "ACCBB4762CF23AA35690CC"
        }
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_put_mock_data())
@patch('chalicelib.player_route.UpdateProfileInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_put_player(client, resource, run):
    result = put_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_put_mock_data())
@patch('chalicelib.player_route.UpdateProfileInteractor.run',
       MagicMock(side_effect=UpdateEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_put_player_raises(client, resource):
    result = put_player()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_profile_request():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch.object(PlayerAdapter, 'get_by_id', return_value=MagicMock())
@patch('chalicelib.player_route.bp_player', make_get_profile_request())
@patch('chalicelib.player_route.GetProfileInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_profile(client, resource, run, get_by_id):
    result = get_my_profile()

    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch.object(PlayerAdapter, 'get_by_id', return_value=MagicMock())
@patch('chalicelib.player_route.bp_player', make_get_profile_request())
@patch('chalicelib.player_route.GetProfileInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_profile_player_not_found(client, resource, get_by_id):
    result = get_my_profile()
    assert result.body['message'] == "Player not found"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch.object(PlayerAdapter, 'get_by_id', return_value=MagicMock())
@patch('chalicelib.player_route.bp_player', make_get_profile_request())
@patch('chalicelib.player_route.GetProfileInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_profile_player_raises(client, resource, get_by_id):
    result = get_my_profile()
    assert result.status_code == 500
    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player(client, resource, run):
    result = get_player_by_id('id1')

    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_raises(client, resource):
    result = get_player_by_id('id1')
    assert result.body['message'] == "Player not found"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player(client, resource, run):
    result = get_all_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_raises(client, resource):
    result = get_all_player()

    assert result.body['message'] == "No player found"
    assert result.body['status'] == "error"
    assert result.status_code == 404


def make_post_mock_data_without_authorization():
    payload = """{
        "user":{
            "name": "Anselmo Lira",
            "email": "playerstars@playerstars.com.br",
            "birth_date": "16/12/1986",
            "street": "Rua José de Figueiredo",
            "street_number": "192",
            "street_complement": "Blocos 29, 30",
            "neighborhood": "Barra da Tijuca",
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "country": "Brasil",
            "postal_code": "22333-000",
            "phone_number": "(21) 99663-6963",
            "cpf": "123.456.789-00",
            "nickname": "anselmo.lira",
            "profile_image": "ACCBB4762CF23AA35690CC"
        },
        "promo_code": "ABC123",
        "favorites": [],
        "red_star_balance": 123,
        "golden_star_balance": 4321,
        "consoles": [
            {
                "entity_id": "1",
                "name": "PS 4",
                "logo_path": "/images/ps4.png",
                "tag_name": "007"
            },
            {
                "entity_id": "11",
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "tag_name": "mario",
                "games": []
            }
        ],
        "states_regions": [],
        "countries_regions": []
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict()))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_mock_data_without_authorization())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player_no_authorization_raises(client, resource, run):
    with pytest.raises(TokenNotFoundException) as excinfo:
        post_player()
    assert str(excinfo.value) == 'Token not found on JWT'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.GetAllFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends(client, resource, run):
    result = get_friends_route('123123')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


def make_get_friends_mock_data():
    return MagicMock(
        current_request=MagicMock(headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_get_friends_mock_data())
@patch('chalicelib.player_route.GetAllFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends_v2(client, resource, run):
    result = get_friends_route_v2()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_get_friends_mock_data())
@patch('chalicelib.player_route.GetAllFriendsInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends_v2_raises(client, resource):
    result = get_friends_route_v2()
    assert result.status_code == 500
    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.GetAllFriendsInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends_not_found(client, resource):
    result = get_friends_route('123123')

    assert result.body['message'] == "Favorites not found"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.GetAllFriendsInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends_raises(client, resource):
    result = get_friends_route('123123')
    assert result.status_code == 500
    assert result.body['message'] == "oops"
    assert result.body['status'] == "error"


def make_post_friends_mock_data():
    json = {
        "friends": ['gluglu', 'yeahyeah']
    }
    return MagicMock(current_request=MagicMock(
        json_body=json, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_friends(client, resource, run):
    result = post_friend_route('12132123')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run',
       MagicMock(side_effect=SaveFriendsException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_friends_raises(client, resource):
    result = post_friend_route('123123')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_friends_raises2(client, resource):
    result = post_friend_route('123123')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_friends_v2(client, resource, run):
    result = post_friend_route_v2()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_friends_v2_raises(client, resource, run):
    result = post_friend_route_v2()
    run.assert_called_once()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_friends(client, resource, run):
    result = delete_friend_route('12132123')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_friends_raises(client, resource, run):
    result = delete_friend_route('12132123')
    run.assert_called_once()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_friends_v2(client, resource, run):
    result = delete_friend_route_v2()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_friends_mock_data())
@patch('chalicelib.player_route.AlterFriendsInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_friends_v2_raises(client, resource, run):
    result = delete_friend_route_v2()
    run.assert_called_once()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_get_teams_by_user_mock_data():
    payload = {
        'player_id': 'pl11'
    }
    return MagicMock(
        current_request=MagicMock(
            json_body=payload,
            headers=dict(
                AUTHORIZATION=jwt,
                get_actives=True,
                get_inactives=True,
                get_i_invited=True,
                get_id_accepted=True)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_get_teams_by_user_mock_data())
@patch('chalicelib.team_route.GetTeamByUserInteractor.run',
       return_value=[{'name': 'Stormianos'}])
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team_by_user(client, resource, run):
    result = get_all_teams_from_player()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


def make_get_teams_by_user_mock_data2():
    return MagicMock(
        current_request=MagicMock(headers=dict(
            AUTHORIZATION=jwt), query_params=None))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_get_teams_by_user_mock_data2())
@patch('chalicelib.team_route.GetTeamByUserInteractor.run',
       return_value=[{'name': 'Stormianos'}])
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team_by_user2(client, resource, run):
    result = get_all_teams_from_player()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_get_teams_by_user_mock_data())
@patch('chalicelib.team_route.GetTeamByUserInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_team_by_user_raises(client, resource, run):
    result = get_all_teams_from_player()
    run.assert_called_once()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_user_data_mock_data():
    payload = """{
        "user":{
            "name": "Anselmo Lira",
            "email": "playerstars@playerstars.com.br",
            "birth_date": "16/12/1986",
            "street": "Rua José de Figueiredo",
            "street_number": "192",
            "street_complement": "Blocos 29, 30",
            "neighborhood": "Barra da Tijuca",
            "city": "Rio de Janeiro",
            "state": "Rio de Janeiro",
            "country": "Brasil",
            "postal_code": "22333-000",
            "phone_number": "(21) 99663-6963",
            "cpf": "123.456.789-00",
            "nickname": "anselmo.lira",
            "profile_image": "ACCBB4762CF23AA35690CC"
        }
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_user_data_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_user_data_player(client, resource, run):
    result = post_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


def make_post_console_mock_data():
    payload = """{
        "entity_id": "id13423",
        "consoles": [
            {
                "entity_id": "1",
                "name": "PS 4",
                "logo_path": "/images/ps4.png",
                "tag_name": "007"
            },
            {
                "entity_id": "11",
                "name": "Xbox",
                "logo_path": "/images/xbox.png",
                "tag_name": "mario",
                "games": []
            }
        ]
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_user_data_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_data_route(client, resource, run):
    result = post_console_data_route()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_console_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_data_route_raises(client, resource):
    result = post_console_data_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', make_post_console_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_console_data_route_raises2(client, resource):
    result = post_console_data_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_accept_terms_mock_data():
    payload = """{
        "entity_id": "id1234123",
        "terms": true
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_terms_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_terms_player(client, resource, run):
    result = post_accept_terms_route()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_terms_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_terms_route_raises(client, resource):
    result = post_accept_terms_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_terms_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_terms_route_raises2(client, resource):
    result = post_accept_terms_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def make_post_accept_invite_mock_data():
    payload = """{
        "team_id": "id1234123",
        "accept_invite": true
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_invite_mock_data())
@patch('chalicelib.player_route.AcceptTeamInvitationInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_team_invite_player(client, resource, run):
    result = accept_team_invitation_route()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_invite_mock_data())
@patch('chalicelib.player_route.AcceptTeamInvitationInteractor.run',
       MagicMock(side_effect=AcceptTeamInvitationException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_team_invite_raises(client, resource):
    result = accept_team_invitation_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       make_post_accept_invite_mock_data())
@patch('chalicelib.player_route.AcceptTeamInvitationInteractor.run',
       MagicMock(side_effect=Exception('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_accept_team_invite_raises2(client, resource):
    result = accept_team_invitation_route()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


def query_params():
    return {
        'console_id': '123',
        'game_id': 'id1234'
    }


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(query_params=query_params())))
@patch('chalicelib.player_route.GetPlayersByConsoleGameInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_by_console(client, resource, run):
    result = get_all_player()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(query_params=query_params())))
@patch('chalicelib.player_route.GetPlayersByConsoleGameInteractor.run',
       return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_by_console_empty(client, resource, run):
    result = get_all_player()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert result.body['message'] == 'Nenhum player encontrado para o' \
                                     ' console: 123 e o game:id1234'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(query_params=query_params())))
@patch('chalicelib.player_route.GetPlayersByConsoleGameInteractor.run',
       side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_by_console_raises(client, resource, run):
    result = get_all_player()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


def convert_star_json():
    payload = """{
        "gold_stars": 3,
        "red_stars": 300
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(
        json_body=data, headers=dict(AUTHORIZATION=jwt)))


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', convert_star_json())
@patch('chalicelib.player_route.SaveConvertedStarsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_converted_star(client, resource, run):
    result = convert_star_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player', convert_star_json())
@patch('chalicelib.player_route.SaveConvertedStarsInteractor.run',
       side_effect=SaveConvertedStarsException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_converted_star_raises(client, resource, run):
    result = convert_star_route()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


def query_params_ranking():
    return {
        'console_id': '123',
        'game_id': 'id1234',
        'pagination_page': 1,
        'pagination_per_page': 10
    }


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params_ranking(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetRankingByConsoleGameInteractor.run',
       return_value=(MagicMock(), MagicMock()))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_ranking(client, resource, run):
    result = get_ranking_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 206


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params_ranking(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetRankingByConsoleGameInteractor.run',
       side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_ranking_error(client, resource, run):
    result = get_ranking_route()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params_ranking(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetRankingByConsoleGameInteractor.run',
       return_value=(None, None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_ranking_not_found(client, resource, run):
    result = get_ranking_route()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert result.body['message'] == \
        'Player 8ad1635f-2263-4dda-879a-bd24b5d9732f ranking not found'


####
# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetPlayerConsolesInteractor.run',
       return_value=(MagicMock()))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_consoles(client, resource, run):
    result = get_player_consoles()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetPlayerConsolesInteractor.run',
       side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_consoles_error(client, resource, run):
    result = get_player_consoles()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetPlayerConsolesInteractor.run',
       return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_consoles_not_found(client, resource, run):
    result = get_player_consoles()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert result.body['message'] == \
        'Player 8ad1635f-2263-4dda-879a-bd24b5d9732f consoles not found'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetFriendsByConsoleGameInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_by_console(client, resource, run):
    result = get_friends_by_console_game_route()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetFriendsByConsoleGameInteractor.run',
       return_value=None)
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_by_console_empty(client, resource, run):
    result = get_friends_by_console_game_route()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert 'Nenhum amigo encontrado para o console' in result.body['message']


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           query_params=query_params(),
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetFriendsByConsoleGameInteractor.run',
       side_effect=BaseException('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_friends_by_console_raises(client, resource, run):
    result = get_friends_by_console_game_route()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetAcceptedTeamsByUserInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_accepted_teams_from_player(client, resource, run):
    result = get_accepted_teams_from_player()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetAcceptedTeamsByUserInteractor.run',
       return_value=[])
@patch('boto3.resource')
@patch('boto3.client')
def test_get_accepted_teams_from_player_empty(client, resource, run):
    result = get_accepted_teams_from_player()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 404
    assert 'No Accepted teams found for user: ' \
           '8ad1635f-2263-4dda-879a-bd24b5d9732f'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.bp_player',
       MagicMock(current_request=MagicMock(
           headers=dict(AUTHORIZATION=jwt))))
@patch('chalicelib.player_route.GetAcceptedTeamsByUserInteractor.run',
       side_effect=Exception('oops'))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_accepted_teams_from_player_raises(client, resource, run):
    result = get_accepted_teams_from_player()
    run.assert_called_once()
    assert result.body['status'] == 'error'
    assert result.status_code == 500
    assert result.body['message'] == 'oops'
