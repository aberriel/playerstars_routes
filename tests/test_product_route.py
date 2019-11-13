from playerstars_interactors import SaveEntityException
from unittest.mock import MagicMock, patch
from chalicelib import get_all_product, post_product
import json


@patch('chalicelib.product_route.GetAllProductsInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_product(client, resource, run):
    result = get_all_product()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.product_route.GetAllProductsInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_product_not_found(client, resource):
    result = get_all_product()

    assert result.body['message'] == 'No product found'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


def make_post_mock_data():
    payload = """{
    "price": 1290,
    "description": "Teste Playerstars",
    "star_value": 200,
    "star_type": "gold"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


# noinspection PyUnusedLocal
@patch('chalicelib.product_route.bp_product',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_post_product(client, resource, run):
    result = post_product()

    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 201


@patch('chalicelib.product_route.bp_product',
       make_post_mock_data())
@patch('chalicelib.basic_entity_route.BasicPostInteractor.run',
       MagicMock(side_effect=SaveEntityException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_post_product_raises(client, resource):
    result = post_product()

    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
