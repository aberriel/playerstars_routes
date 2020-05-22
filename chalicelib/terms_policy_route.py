from chalice import Blueprint
from playerstars_adapters import TermsAdapter, PrivacyPolicyAdapter
from playerstars_domain import Terms, PrivacyPolicy
from chalicelib.chalice_support import private_get
from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings

bp_terms = Blueprint(__name__)


def terms_router():
    adapter = TermsAdapter(
        Settings.TERMS_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Terms, 'terms')


@bp_terms.route('/{entity_id}', **private_get())
def get_terms_by_id(entity_id):
    return terms_router().get_by_id(entity_id)


bp_policy = Blueprint(__name__)


def policy_router():
    adapter = PrivacyPolicyAdapter(
        Settings.PRIVACY_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, PrivacyPolicy, 'privacy-policy')


@bp_policy.route('/{entity_id}', **private_get())
def get_policy_by_id(entity_id):
    return policy_router().get_by_id(entity_id)
