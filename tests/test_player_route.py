from playerstars_interactors import SaveEntityException
from chalicelib.player_route import (
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
    jwt = "eyJraWQiOiI5bisrRW95QnVjUjRoTHRjUnRHeG5yb0YyTkFBT0I0emdxVFlRbXN" \
          "hWEc4PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4YWQxNjM1Zi0yMjYzLTRkZG" \
          "EtODc5YS1iZDI0YjVkOTczMmYiLCJhdWQiOiJhNHUwbG4wMml1bmc1cDcybmtmd" \
          "HJrczhtIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV2ZW50X2lkIjoiMmRlYTQ1" \
          "M2QtNmViOS00MzZjLTgzYTUtOTNkYjc4ZjUwMTljIiwidG9rZW5fdXNlIjoiaWQ" \
          "iLCJhdXRoX3RpbWUiOjE1NjgyMjQ2MjksImlzcyI6Imh0dHBzOlwvXC9jb2duaX" \
          "RvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2tPdXFPe" \
          "GUxYiIsImNvZ25pdG86dXNlcm5hbWUiOiI4YWQxNjM1Zi0yMjYzLTRkZGEtODc5" \
          "YS1iZDI0YjVkOTczMmYiLCJleHAiOjE1NjgyMzE3OTgsImlhdCI6MTU2ODIyODE" \
          "5OCwiZW1haWwiOiJ2b3ZvZGVnQGJlLWJyZWF0aHRha2luZy5uZXQifQ.Il5Xmnb" \
          "JGVCh1j7sSgQ1QlGW6K8oK9SQG1pqybFY8_Yw2n_v021ZfVXCwXhkQW1_i04n3n" \
          "jBeJMzsyt8hYDyXQFiU6e-3pVyyxkSr6ST3KtHqRcQ9R8kkVM5Y0mXGIyiJ-_CO" \
          "Z-fdmcpCTajc3DEM-b9okJVv1myIaJITO0b0j57Nu62U6GYnwL9ql-lvF--NYOf" \
          "yFV9WoybqVJ06TKqks4XjpkCoHP9-pO3-6GqB02leL-mL_U9Jcu-yO6ANVuXn12" \
          "v8ZCNJjWqNY-LNzdfRShk8GUf92XWxzAu9BuVM9cfKiQL-xznpWMBnuuAY5MjSO" \
          "_oWDQnH3PZEd_pLdPsLg"
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
