from marshmallow import Schema, fields
from uuid import uuid4


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
