from chalicelib import get_terms, get_policy
from chalicelib.terms_policy_route import terms_router, policy_router
from unittest.mock import patch
from chalicelib.settings import Settings
from playerstars_domain import Terms, PrivacyPolicy


@patch('chalicelib.terms_policy_route.TermsAdapter')
@patch('chalicelib.terms_policy_route.BasicEntityRoute')
def test_terms_router(ber, adapter):
    router = terms_router()
    assert router
    adapter.assert_called_with(
        Settings.TERMS_TABLE_NAME, Settings.DYNAMODB_URL)
    ber.assert_called_with(adapter(), Terms, 'terms')


@patch('chalicelib.terms_policy_route.terms_router')
def test_get_terms_by_id(router):
    response = get_terms()
    assert response
    router().get_all.assert_called_once()


@patch('chalicelib.terms_policy_route.PrivacyPolicyAdapter')
@patch('chalicelib.terms_policy_route.BasicEntityRoute')
def test_policy_router(ber, adapter):
    router = policy_router()
    assert router
    adapter.assert_called_with(
        Settings.PRIVACY_TABLE_NAME, Settings.DYNAMODB_URL)
    ber.assert_called_with(adapter(), PrivacyPolicy, 'privacy-policy')


@patch('chalicelib.terms_policy_route.policy_router')
def test_get_policy_by_id(router):
    response = get_policy()
    assert response
    router().get_all.assert_called_once()
