from playerstars_interactors import SaveEntityException, SaveFriendsException
from chalicelib.player_route import (
    get_all_player,
    get_player_by_id,
    post_player,
    get_my_profile,
    get_friends_route,
    post_friend_route,
    delete_friend_route
)
from tests.test_utils import jwt
from unittest.mock import MagicMock, patch
import json
import pytest
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
        "blue_star_balance": 123,
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
def test_get_profile_raises(client, resource, get_by_id):
    result = get_my_profile()
    assert result.body['message'] == "Player não encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


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
    assert result.body['message'] == "Player não encontrado"
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

    assert result.body['message'] == "Nenhum player encontrado"
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
        "blue_star_balance": 123,
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
    assert str(excinfo.value) == 'Token não encontrado no JWT'


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.GetAllFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends(client, resource, run):
    result = get_friends_route('123123')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.player_route.GetAllFriendsInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_friends_raises(client, resource):
    result = get_friends_route('123123')

    assert result.body['message'] == "Favoritos não enontrados"
    assert result.body['status'] == "error"
    assert result.status_code == 404


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
@patch('chalicelib.player_route.AlterFriendsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_delete_friends(client, resource, run):
    result = delete_friend_route('12132123')
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201
