from unittest.mock import MagicMock, patch
from playerstars_routes import get_all_region_state


@patch('playerstars_routes.region_state_route.'
       'GetAllStateRegionsInteractor.run',
       MagicMock(return_value='ok'))
def test_get_all_region_state():
    result = get_all_region_state()

    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('playerstars_routes.region_state_route.'
       'GetAllStateRegionsInteractor.run',
       MagicMock(return_value=None))
def teste_get_all_region_country_not_found():
    result = get_all_region_state()

    assert result.body['status'] == 'error'
    assert result.status_code == 404
