from chalicelib.basic_entity_route import BasicEntityRoute
from unittest.mock import MagicMock


def query_params():
    return {
        'pagination_page': 1,
        'pagination_per_page': 10
    }


def test_get_all():
    ber = BasicEntityRoute(
        adapter_instance=MagicMock(), entity_class=MagicMock(),
        entity_name='teste')
    response = ber.get_all(
        query_params=query_params(), paginate=True, _filter=False)
    assert response.status_code == 404
    assert response.body['status'] == 'error'
    assert response.body['message'] == 'No teste found'
