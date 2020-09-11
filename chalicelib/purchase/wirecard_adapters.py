from playerstars_wirecard import (
    CreditCardAdapter,
    PlanAdapter,
    SubscriberAdapter,
    SubscriptionAdapter)

from chalicelib.settings import Settings


def get_credit_card_adapter(customer_id):
    return CreditCardAdapter(
        auth_user=Settings.WIRECARD_API_USER,
        auth_password=Settings.WIRECARD_API_PASSWORD,
        url_base=Settings.WIRECARD_API_URL_BASE,
        customer_code=customer_id)


def get_plan_adapter():
    return PlanAdapter(
        auth_user=Settings.WIRECARD_API_USER,
        auth_password=Settings.WIRECARD_API_PASSWORD,
        url_base=Settings.WIRECARD_API_URL_BASE)


def get_subscriber_adapter():
    return SubscriberAdapter(
        auth_user=Settings.WIRECARD_API_USER,
        auth_password=Settings.WIRECARD_API_PASSWORD,
        url_base=Settings.WIRECARD_API_URL_BASE)


def get_subscription_adapter():
    return SubscriptionAdapter(
        auth_user=Settings.WIRECARD_API_USER,
        auth_password=Settings.WIRECARD_API_PASSWORD,
        url_base=Settings.WIRECARD_API_URL_BASE)
