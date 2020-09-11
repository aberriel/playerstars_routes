from chalicelib.purchase.post_webhook_wirecard import (
    get_player_adapter,
    mount_webhook_adapters,
    post_webhook,
    process_received_webhook)
from unittest.mock import patch, MagicMock

prefix = 'chalicelib.purchase.post_webhook_wirecard'


@patch(f'{prefix}.Settings')
@patch(f'{prefix}.PlayerAdapter')
def test_get_player_adapter(player_adapter_mock, settings_mock):
    player_adapter = get_player_adapter()
    player_adapter_mock.assert_called_once_with(
        table_name=settings_mock.PLAYER_TABLE_NAME,
        db_endpoint=settings_mock.DYNAMODB_URL)
    assert player_adapter == player_adapter_mock()


@patch(f'{prefix}.WebhookProcessorAdapters')
@patch(f'{prefix}.get_player_adapter')
@patch(f'{prefix}.get_subscription_adapter')
@patch(f'{prefix}.get_plan_adapter')
def test_mount_interactor_adapters(get_plan_adapter_mock,
                                   get_subscription_adapter_mock,
                                   get_player_adapter_mock,
                                   interactor_adapters_mock):
    interactor_adapters = mount_webhook_adapters()
    get_plan_adapter_mock.assert_called_once()
    get_subscription_adapter_mock.assert_called_once()
    get_player_adapter_mock.assert_called_once()
    interactor_adapters_mock.assert_called_once_with(
        player_adapter=get_player_adapter_mock(),
        subscription_adapter=get_subscription_adapter_mock(),
        plan_adapter=get_plan_adapter_mock())
    assert interactor_adapters == interactor_adapters_mock()


@patch(f'{prefix}.bp_webhook_wirecard')
@patch(f'{prefix}.process_received_webhook')
def test_post_webhook(process_received_webhook_mock,
                      bp_webhook_wirecard_mock):
    mock_data = bp_webhook_wirecard_mock.current_request.json_body
    response = post_webhook()
    process_received_webhook_mock.assert_called_once_with(
        webhook_data=mock_data)
    assert response == process_received_webhook_mock()


@patch(f'{prefix}.ReceiveWebhookInteractor')
@patch(f'{prefix}.mount_webhook_adapters')
@patch(f'{prefix}.success')
@patch(f'{prefix}.server_error')
def test_process_received_webhook(server_error_mock,
                                  success_mock,
                                  mount_webhook_adapters_mock,
                                  interactor_mock):
    webhook_json = MagicMock()
    response = process_received_webhook(webhook_json)
    mount_webhook_adapters_mock.assert_called_once()
    interactor_mock.assert_called_once_with(
        webhook_json=webhook_json,
        adapters=mount_webhook_adapters_mock())
    interactor_mock().run.assert_called_once()
    success_mock.assert_called_once_with(interactor_mock().run()())
    server_error_mock.assert_not_called()
    assert response == success_mock()


@patch(f'{prefix}.ReceiveWebhookInteractor')
@patch(f'{prefix}.mount_webhook_adapters')
@patch(f'{prefix}.success')
@patch(f'{prefix}.server_error')
def test_process_received_webhook_fails(server_error_mock,
                                        success_mock,
                                        mount_webhook_adapters_mock,
                                        interactor_mock):
    interactor_mock().run = MagicMock(side_effect=Exception('oops'))
    webhook_json = MagicMock()
    response = process_received_webhook(webhook_json)
    mount_webhook_adapters_mock.assert_called_once()
    interactor_mock.assert_called_with(
        webhook_json=webhook_json,
        adapters=mount_webhook_adapters_mock())
    interactor_mock().run.assert_called_once()
    success_mock.assert_not_called()
    server_error_mock.assert_called_once_with('Exception: oops')
    assert response == server_error_mock()
