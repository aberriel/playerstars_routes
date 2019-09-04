from playerstars_interactors import SaveEntityException
from playerstars_routes.player_route import (
    get_all_player,
    get_player_by_id,
    post_player
)
from unittest.mock import MagicMock, patch
import json


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
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('playerstars_routes.player_route.bp_player', make_post_mock_data())
@patch('playerstars_routes.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player(client, resource, run):
    result = post_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 201


# noinspection PyUnusedLocal
@patch('playerstars_routes.player_route.bp_player', make_post_mock_data())
@patch('playerstars_routes.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_player_raises(client, resource):
    result = post_player()
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('playerstars_routes.basic_entity_route.BasicGetInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player(client, resource, run):
    result = get_player_by_id('id1')

    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.basic_entity_route.BasicGetInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_player_raises(client, resource):
    result = get_player_by_id('id1')
    assert result.body['message'] == "Player não encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('playerstars_routes.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player(client, resource, run):
    result = get_all_player()
    run.assert_called_once()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_player_raises(client, resource):
    result = get_all_player()

    assert result.body['message'] == "Nenhum player encontrado"
    assert result.body['status'] == "error"
    assert result.status_code == 404
