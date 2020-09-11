from chalicelib.purchase.post_red_stars_purchase import (
    get_player_adapter,
    mount_interactor_adapters,
    post_wirecard_purchase,
    purchase_red_stars)
from playerstars_interactors import RedStarsPurchaseException
from unittest.mock import patch, MagicMock

prefix = 'chalicelib.purchase.post_red_stars_purchase'


@patch(f'{prefix}.Settings')
@patch(f'{prefix}.PlayerAdapter')
def test_get_player_adapter(player_adapter_mock, settings_mock):
    player_adapter = get_player_adapter()
    player_adapter_mock.assert_called_once_with(
        table_name=settings_mock.PLAYER_TABLE_NAME,
        db_endpoint=settings_mock.DYNAMODB_URL)
    assert player_adapter == player_adapter_mock()


@patch(f'{prefix}.RedStarPurchaseInteractorAdapters')
@patch(f'{prefix}.get_credit_card_adapter')
@patch(f'{prefix}.get_plan_adapter')
@patch(f'{prefix}.get_player_adapter')
@patch(f'{prefix}.get_subscriber_adapter')
@patch(f'{prefix}.get_subscription_adapter')
def test_mount_interactor_adapters(get_subscription_adapter_mock,
                                   get_subscriber_adapter_mock,
                                   get_player_adapter_mock,
                                   get_plan_adapter_mock,
                                   get_credit_card_adapter_mock,
                                   interactor_adapters_mock):
    interactor_adapters = mount_interactor_adapters('player123')
    get_credit_card_adapter_mock.assert_called_once_with('player123')
    get_plan_adapter_mock.assert_called_once()
    get_player_adapter_mock.assert_called_once()
    get_subscriber_adapter_mock.assert_called_once()
    get_subscription_adapter_mock.assert_called_once()
    interactor_adapters_mock.assert_called_once_with(
        credit_card_adapter=get_credit_card_adapter_mock(),
        plan_adapter=get_plan_adapter_mock(),
        player_adapter=get_player_adapter_mock(),
        subscriber_adapter=get_subscriber_adapter_mock(),
        subscription_adapter=get_subscription_adapter_mock())
    assert interactor_adapters == interactor_adapters_mock()


@patch(f'{prefix}.bp_wirecard')
@patch(f'{prefix}.get_user_id_from_jwt')
@patch(f'{prefix}.purchase_red_stars')
def test_post_wirecard_purchase(purchase_red_stars_mock,
                                get_user_id_from_jwt_mock,
                                bp_wirecard_mock):
    post_wirecard_purchase()
    mock_data = bp_wirecard_mock.current_request.json_body
    mock_player_id = get_user_id_from_jwt_mock()
    mock_data.update.assert_called_with({'code': mock_player_id})
    purchase_red_stars_mock.assert_called_once_with(
        json_data=mock_data,
        player_id=mock_player_id)


@patch(f'{prefix}.mount_interactor_adapters')
@patch(f'{prefix}.RedStarsPurchaseRequestModel')
@patch(f'{prefix}.RedStarsPurchaseInteractor')
@patch(f'{prefix}.created')
@patch(f'{prefix}.server_error')
def test_purchase_red_stars(server_error_mock,
                            created_mock,
                            interactor_mock,
                            request_model_mock,
                            mount_adapters_mock):
    json_data = MagicMock()
    player_id = MagicMock()
    response = purchase_red_stars(json_data, player_id)

    mount_adapters_mock.assert_called_once_with(player_id)
    request_model_mock.assert_called_once_with(json_data)
    interactor_mock.assert_called_once_with(
        adapters=mount_adapters_mock(),
        request=request_model_mock())
    interactor_mock().run.assert_called_once()
    created_mock.assert_called_once_with(interactor_mock().run()())
    server_error_mock.assert_not_called()
    assert response == created_mock()


@patch(f'{prefix}.mount_interactor_adapters')
@patch(f'{prefix}.RedStarsPurchaseRequestModel')
@patch(f'{prefix}.RedStarsPurchaseInteractor')
@patch(f'{prefix}.server_error')
@patch(f'{prefix}.created')
def test_purchase_red_stars_fail(created_mock,
                                 server_error_mock,
                                 interactor_mock,
                                 request_model_mock,
                                 mount_adapters_mock):
    interactor_mock().run = \
        MagicMock(side_effect=RedStarsPurchaseException('oops'))
    json_data = MagicMock()
    player_id = MagicMock()
    response = purchase_red_stars(json_data, player_id)
    mount_adapters_mock.assert_called_once_with(player_id)
    request_model_mock.assert_called_once_with(json_data)
    interactor_mock.assert_called_with(
        adapters=mount_adapters_mock(),
        request=request_model_mock())
    interactor_mock().run.assert_called_once()
    created_mock.assert_not_called()
    server_error_mock.assert_called_once_with('oops')
    assert response == server_error_mock()
