# from unittest.mock import MagicMock, patch
from .test_utils import FakeDomain, FakeAdapter
from app import index
from chalice_support import success
from chalicelib.routes import home
from unittest.mock import MagicMock, patch

import json
import logging


class FakePostRequestModel:
    _id = None
    nome = None
    email = None
    pais = None

    def __init__(self, _id, nome, email, pais):
        self._id = _id
        self.nome = nome
        self.email = email
        self.pais = pais


class FakePostResponseModel:
    def __init__(self,
                 request: FakePostRequestModel,
                 logger=logging.getLogger(__name__)):
        self.request = request
        self.logger = logger

    def _init_domain(self):
        fake_domain = FakeDomain(
            _id=self.request._id,
            nome=self.request.nome,
            email=self.request.email,
            pais=self.request.pais)
        return fake_domain

    def run(self):
        fake_adapter = FakeAdapter()
        fake_domain = self._init_domain()
        fake_domain.set_adapter(fake_adapter)
        return fake_domain.save()


class SaveFakeException(BaseException):
    pass


def post_fake():
    from app import app
    body = app.current_request.json_body
    request = FakePostRequestModel(
        _id=body.get('_id'),
        nome=body.get('nome'),
        email=body.get('email'),
        pais=body.get('pais')
    )

    response = FakePostResponseModel(request)
    result = response.run()
    return success(result)


def make_post_mock_data():
    payload = """{
        "email":"user@dom.com",
        "_id":"bd0f6125-b944-43b0-adfb-455b493ea0f8",
        "nome":"USUARIO",
        "pais":"Brasiu"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('app.app', make_post_mock_data())
def test_post_fake():
    result = post_fake()
    assert result.body['status'] == 'success'
    assert result.status_code == 200
    assert result.body['data'] == "bd0f6125-b944-43b0-adfb-455b493ea0f8"


def test_get_root():
    result = index()

    assert result['status'] == 'ok'
    assert result['data'] == 'PlayerStars is alive!!'


def test_home():
    result = home()
    assert result.status_code == 404
