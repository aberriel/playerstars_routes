from unittest.mock import MagicMock, patch
from chalicelib import get_all_product


@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_product(client, resource, run):
    result = get_all_product()
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def teste_get_all_product_not_found(client, resource):
    result = get_all_product()

    assert result.body['message'] == 'Nenhum product encontrado'
    assert result.body['status'] == 'error'
    assert result.status_code == 404
