from chalicelib.purchase.post_google_purchase import (
    get_player_adapter,
    notify_google_purchase,
    post_google_purchase_notify)
from playerstars_interactors import PostPurchaseNotificationByGoogleException
from unittest.mock import patch, MagicMock


prefix = 'chalicelib.purchase.post_google_purchase'


@patch(f'{prefix}.Settings')
@patch(f'{prefix}.PlayerAdapter')
def test_get_player_adapter(player_adapter_mock, settings_mock):
    player_adapter = get_player_adapter()
    player_adapter_mock.assert_called_once_with(
        table_name=settings_mock.PLAYER_TABLE_NAME,
        db_endpoint=settings_mock.DYNAMODB_URL)
    assert player_adapter == player_adapter_mock()


@patch(f'{prefix}.bp_google')
@patch(f'{prefix}.get_user_id_from_jwt')
@patch(f'{prefix}.notify_google_purchase')
def test_post_google_purchase_notify(notify_google_purchase_mock,
                                     get_user_id_from_jwt_mock,
                                     bp_google_mock):
    response = post_google_purchase_notify()
    mock_data = bp_google_mock.current_request.json_body
    mock_player_id = get_user_id_from_jwt_mock()
    mock_data.update.assert_called_with({'player_id': mock_player_id})
    notify_google_purchase_mock.assert_called_once_with(mock_data)
    assert response == notify_google_purchase_mock()


@patch(f'{prefix}.PostPurchaseNotificationByGoogleRequestModel')
@patch(f'{prefix}.PostPurchaseNotificationByGoogleInteractor')
@patch(f'{prefix}.get_player_adapter')
@patch(f'{prefix}.success')
@patch(f'{prefix}.server_error')
def test_notify_google_purchase(server_error_mock,
                                success_mock,
                                get_player_adapter_mock,
                                interactor_mock,
                                request_model_mock):
    json_data = MagicMock()
    response = notify_google_purchase(json_data)
    get_player_adapter_mock.assert_called_once()
    request_model_mock.assert_called_with(json_data)
    interactor_mock.assert_called_once_with(
        request=request_model_mock(),
        player_adapter=get_player_adapter_mock())
    interactor_mock().run.assert_called_once()
    server_error_mock.assert_not_called()
    success_mock.assert_called_once_with(
        interactor_mock().run()())
    assert response == success_mock()


@patch(f'{prefix}.PostPurchaseNotificationByGoogleRequestModel')
@patch(f'{prefix}.PostPurchaseNotificationByGoogleInteractor')
@patch(f'{prefix}.get_player_adapter')
@patch(f'{prefix}.success')
@patch(f'{prefix}.server_error')
def test_notify_google_purchase_fails(server_error_mock,
                                      success_mock,
                                      get_player_adapter_mock,
                                      interactor_mock,
                                      request_model_mock):
    interactor_mock().run = \
        MagicMock(
            side_effect=PostPurchaseNotificationByGoogleException('oops'))
    json_data = MagicMock()

    response = notify_google_purchase(json_data)
    get_player_adapter_mock.assert_called_once()
    request_model_mock.assert_called_with(json_data)
    interactor_mock.assert_called_with(
        request=request_model_mock(),
        player_adapter=get_player_adapter_mock())
    interactor_mock().run.assert_called_once()
    server_error_mock.assert_called_once_with('oops')
    success_mock.assert_not_called()
    assert response == server_error_mock()
