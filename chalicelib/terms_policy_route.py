from chalice import Blueprint
from playerstars_adapters import TermsAdapter, PrivacyPolicyAdapter
from playerstars_domain import Terms, PrivacyPolicy
from chalicelib import BasicEntityRoute
from chalicelib.settings import Settings
from chalicelib.chalice_support.auth import cors

bp_terms = Blueprint(__name__)


def terms_router():
    adapter = TermsAdapter(
        Settings.TERMS_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, Terms, 'terms')


@bp_terms.route('/', methods=['GET'], cors=cors)
def get_terms():
    return terms_router().get_all()


bp_policy = Blueprint(__name__)


def policy_router():
    adapter = PrivacyPolicyAdapter(
        Settings.PRIVACY_TABLE_NAME, Settings.DYNAMODB_URL)
    return BasicEntityRoute(adapter, PrivacyPolicy, 'privacy-policy')


@bp_policy.route('/', methods=['GET'], cors=cors)
def get_policy():
    return policy_router().get_all()
