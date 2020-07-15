from chalicelib.basic_entity_route import BasicEntityRoute
from unittest.mock import MagicMock, patch
from marshmallow import ValidationError


def query_params():
    return {
        'pagination_page': 1,
        'pagination_per_page': 10
    }


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all(client, resource, run):
    ber = BasicEntityRoute(
        adapter_instance=MagicMock(), entity_class=MagicMock(),
        entity_name='teste')
    result = ber.get_all(
        query_params=query_params())
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 206


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(side_effect=BaseException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_raises(boto_client, boto_resource):
    ber = BasicEntityRoute(
        adapter_instance=MagicMock(), entity_class=MagicMock(),
        entity_name='teste')
    result = ber.get_all(
        query_params=query_params())
    assert 'oops' in result.body['message']
    assert result.body['status'] == 'error'
    assert result.status_code == 500


# noinspection PyUnusedLocal
@patch('chalicelib.basic_entity_route.BasicGetAllInteractor.run',
       MagicMock(side_effect=ValidationError('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_consoles_raises_2(boto_client, boto_resource):
    ber = BasicEntityRoute(
        adapter_instance=MagicMock(), entity_class=MagicMock(),
        entity_name='teste')
    result = ber.get_all(
        query_params=query_params())
    assert 'oops' in result.body['message']
    assert result.body['status'] == 'error'
    assert result.status_code == 500
