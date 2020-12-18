from unittest.mock import patch

from chalice_support.basic_routes_tester import BasicChaliceRoutesTester
from playerstars_domain import PreDuel

from chalicelib.admin.preduel_routes import get_preduel_admin_routes, \
    get_preduel_adatper
from chalicelib.settings import Settings

prefix = 'chalicelib.admin.preduel_routes'


def test_preduel_admin_routes():
    bcrt = BasicChaliceRoutesTester(prefix,
                                    get_preduel_adatper,
                                    PreDuel,
                                    get_preduel_admin_routes,
                                    'Blueprint')
    bcrt.do_test()


@patch(f'{prefix}.PreDuelAdapter')
def test_adapter_getter(mock_adapter):
    result = get_preduel_adatper()

    mock_adapter.assert_called_with(Settings.PREDUEL_TABLE_NAME,
                                    Settings.DYNAMODB_URL)

    assert result == mock_adapter()
