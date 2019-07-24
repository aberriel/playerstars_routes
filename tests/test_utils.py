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
        return self.Schema().dump(self)[0]

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
