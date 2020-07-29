from unittest.mock import patch, MagicMock
from uuid import uuid4

import pytest
from marshmallow import Schema, fields
from playerstars_domain import Player

from chalicelib.utils import \
    (check_admin_authorization, UserNotAdminAuthorized,
     UserNotFoundToAuthorize, _replace_dot, make_fields_dot)


@patch('chalicelib.utils.PlayerAdapter')
def test_check_admin(adapter):
    assert not check_admin_authorization('1234')


player = Player.from_json({
    'entity_id': 'af1bf976-b212-42a9-af2a-fc20ed4688de',
    'user': {
        'name': 'Luan Garcia',
        'email': 'luan.garcia@stormsec.com.br',
        'nickname': 'ddeeff',
        'street': 'Rua Mandina',
        'street_number': '35',
        'street_complement': 'casa 1',
        'neighborhood': 'Curicica',
        'city': 'Rio de Janeiro',
        'state': 'Rio de Janeiro',
        'country': 'Brasil',
        'postal_code': '23335-115',
        'date_birth': '1988-12-25',
        'phone_number': '(21) 99155-2323',
        'cpf': '123.456.789-01',
        'profile_image': None
    },
    'player_status': 'AVAILABLE',
    'red_star_balance': 0,
    'golden_star_balance': 5,
    'points': 500,
    'terms': True,
    "is_admin": False,
    "is_blocked": False,
    'consoles': [{
        'console_id': '531f6ee2-dfef-458e-b918-ebf12793fe37',
        'tag_name': 'tag#1',
        'game_points': [{
            'game_id': '0e3bd0f7-e95c-4168-9083-f1859fa73902',
            'victories': 0
        }]
    }],
    'states_regions': [],
    'countries_regions': [],
    'favorites': [],
    'star_transactions': [],
    'star_reservations': [],
    'purchases': []
})


def get_by_id(id):
    return player


@patch('chalicelib.utils.PlayerAdapter',
       return_value=MagicMock(get_by_id=get_by_id))
def test_check_admin_raises(adapter):
    with pytest.raises(UserNotAdminAuthorized) as excinfo:
        check_admin_authorization('1234')
    assert 'Usuário não autorizado como admin' in str(excinfo.value)


def get_by_id2(id):
    return None


@patch('chalicelib.utils.PlayerAdapter',
       return_value=MagicMock(get_by_id=get_by_id2))
def test_check_admin_user_not_found(adapter):
    with pytest.raises(UserNotFoundToAuthorize) as excinfo:
        check_admin_authorization('1234')
    assert 'Usuário não encontrado' in str(excinfo.value)


class FakeDomain:
    def __init__(self, nome, email, pais, _id=None):
        self._id = _id or str(uuid4())
        self.nome = nome
        self.email = email
        self.pais = pais
        self.adapter = None

    def set_adapter(self, adapter):
        self.adapter = adapter

    def to_json(self):
        return self.Schema().dump(self)

    def save(self):
        my_id = self.adapter.save(self.to_json())
        return my_id

    class Schema(Schema):
        _id = fields.String(required=True, allow_none=False)
        email = fields.String(required=True, allow_none=False)
        nome = fields.String(required=True, allow_none=False)
        pais = fields.String(required=True, allow_none=False)


fake_db = dict()


class FakeAdapter:

    def save(self, json_data):
        entity_id = json_data.get('_id', str(uuid4()))
        json_data.update(dict(entity_id=entity_id))
        fake_db.update({entity_id: json_data})
        return entity_id


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


def test_replace_dot():
    mock_field = 'campo.subcampo'

    # noinspection PyProtectedMember
    result = _replace_dot(mock_field)

    assert result == 'campo_dot_subcampo'


def test_make_fields_dot():
    mock_params = dict(sort_field='campo.subcampo',
                       filter_field='outro.sub')

    result = make_fields_dot(mock_params)

    assert result['sort_field'] == 'campo_dot_subcampo'
    assert result['filter_field'] == 'outro_dot_sub'


def test_make_fields_dot_no_params():
    mock_params = dict()

    result = make_fields_dot(mock_params)
    assert result == {}

    mock_params = None
    result = make_fields_dot(mock_params)
    assert result == {}


def test_make_fields_dot_only_sort():
    mock_params = dict(sort_field='campo.subcampo',
                       sort_order='asc',
                       pagination_page=1,
                       pagination_perPage=10)

    # noinspection PyProtectedMember
    result = make_fields_dot(mock_params)

    assert result == {
        'pagination_page': 1,
        'pagination_perPage': 10,
        'sort_field': 'campo_dot_subcampo',
        'sort_order': 'asc'
    }


def test_make_fields_dot_only_filter():
    mock_params = dict(filter_field='campo.subcampo',
                       filter_value='42',
                       pagination_page=1,
                       pagination_perPage=10)

    # noinspection PyProtectedMember
    result = make_fields_dot(mock_params)

    assert result == {
        'pagination_page': 1,
        'pagination_perPage': 10,
        'filter_field': 'campo_dot_subcampo',
        'filter_value': '42'
    }
