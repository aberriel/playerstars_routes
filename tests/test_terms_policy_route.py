from chalicelib import get_terms_by_id, get_policy_by_id
from chalicelib.terms_policy_route import terms_router, policy_router
from unittest.mock import patch


@patch('chalicelib.terms_policy_route.TermsAdapter')
@patch('chalicelib.terms_policy_route.BasicEntityRoute')
def test_terms_router(ber, adapter):
    router = terms_router()
    assert router


@patch('chalicelib.terms_policy_route.terms_router')
def test_get_terms_by_id(router):
    response = get_terms_by_id('entity_id')
    assert response


@patch('chalicelib.terms_policy_route.PrivacyPolicyAdapter')
@patch('chalicelib.terms_policy_route.BasicEntityRoute')
def test_policy_router(ber, adapter):
    router = policy_router()
    assert router


@patch('chalicelib.terms_policy_route.policy_router')
def test_get_policy_by_id(router):
    response = get_policy_by_id('entity_id')
    assert response
