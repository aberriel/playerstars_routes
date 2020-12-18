from unittest.mock import patch

from chalicelib.dashboard.dashboard_adapter import DashboardAdapter, \
    NullDashboardAdapter
from chalicelib.dashboard.dashboard_entity import DashboardEntity


@patch('clapy_dynamodb_adapter.basic_dynamodb_adapter'
       '.BasicDynamodbAdapter.__init__')
def test_dashboard_adapter(mock_init):
    adapter = DashboardAdapter(table_name='dashboard_table')

    mock_init.assert_called_with(table_name='dashboard_table',
                                 db_endpoint=None,
                                 adapted_class=DashboardEntity)
    assert isinstance(adapter, DashboardAdapter)


def test_null_dashboard_adapter():
    nadapter = NullDashboardAdapter('nada')
    assert nadapter.list_all() == []
    assert nadapter.get_by_id('algo') is None
    assert nadapter.save('nada') == ''
    assert nadapter.delete('nada') == 'nada'
    assert nadapter.filter() == []
