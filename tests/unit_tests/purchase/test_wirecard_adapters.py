from chalicelib.purchase.wirecard_adapters import (
    get_credit_card_adapter,
    get_plan_adapter,
    get_subscriber_adapter,
    get_subscription_adapter)

from unittest.mock import patch


prefix = 'chalicelib.purchase.wirecard_adapters'


@patch(f'{prefix}.CreditCardAdapter')
@patch(f'{prefix}.Settings')
def test_credit_card_adapter(settings_mock, credit_card_adapter_mock):
    credit_card_adapter = get_credit_card_adapter('player123')
    credit_card_adapter_mock.assert_called_once_with(
        auth_user=settings_mock.WIRECARD_API_USER,
        auth_password=settings_mock.WIRECARD_API_PASSWORD,
        url_base=settings_mock.WIRECARD_API_URL_BASE,
        customer_code='player123')
    assert credit_card_adapter == credit_card_adapter_mock()


@patch(f'{prefix}.PlanAdapter')
@patch(f'{prefix}.Settings')
def test_plan_adapter(settings_mock, plan_adapter_mock):
    plan_adapter = get_plan_adapter()
    plan_adapter_mock.assert_called_once_with(
        auth_user=settings_mock.WIRECARD_API_USER,
        auth_password=settings_mock.WIRECARD_API_PASSWORD,
        url_base=settings_mock.WIRECARD_API_URL_BASE)
    assert plan_adapter == plan_adapter_mock()


@patch(f'{prefix}.SubscriberAdapter')
@patch(f'{prefix}.Settings')
def test_subscriber_adapter(settings_mock, subscriber_adapter_mock):
    subscriber_adapter = get_subscriber_adapter()
    subscriber_adapter_mock.assert_called_once_with(
        auth_user=settings_mock.WIRECARD_API_USER,
        auth_password=settings_mock.WIRECARD_API_PASSWORD,
        url_base=settings_mock.WIRECARD_API_URL_BASE)
    assert subscriber_adapter == subscriber_adapter_mock()


@patch(f'{prefix}.SubscriptionAdapter')
@patch(f'{prefix}.Settings')
def test_subscription_adapter(settings_mock, subscription_adapter_mock):
    subscription_adapter = get_subscription_adapter()
    subscription_adapter_mock.assert_called_once_with(
        auth_user=settings_mock.WIRECARD_API_USER,
        auth_password=settings_mock.WIRECARD_API_PASSWORD,
        url_base=settings_mock.WIRECARD_API_URL_BASE)
    assert subscription_adapter == subscription_adapter_mock()
