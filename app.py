from chalice import Chalice

from chalicelib import root
from chalicelib.settings import Settings
from chalicelib.console_route import bp_console, bp_console_admin
from chalicelib.duel_route import (
    bp_cancel_duel,
    bp_create_duel,
    bp_duel,
    bp_enter_duel,
    bp_inform_invite_timeout,
    bp_match_list)
from chalicelib.duel_scheduled_finisher import duel_scheduled_finisher
from chalicelib.game_route import bp_game, bp_game_by_console
from chalicelib.notification_route import (
    bp_notification,
    bp_notification_read)
from chalicelib.player_route import bp_player, bp_player_by_console
from chalicelib.product_route import bp_plan, bp_product
from chalicelib.purchase_route import bp_purchase
from chalicelib.region_country_route import bp_region_country
from chalicelib.region_state_route import bp_region_state
from chalicelib.mail_routes import (
    bp_contact_email, bp_invitation_email, bp_welcome_email)
from chalicelib.team_route import bp_enter_team, bp_team
from chalicelib.user_admin_route import bp_user_admin
from chalicelib.convert_star_rate_route import bp_convert
from chalicelib.admin_routes import bp_admin
from chalicelib.values_route import bp_value
from chalicelib.terms_policy_route import bp_terms, bp_policy
from chalicelib.tournament.post_tournament_start import tournament_route

app = Chalice(app_name='playerstars')
app.experimental_feature_flags.update(['BLUEPRINTS'])

app.register_blueprint(tournament_route, url_prefix='/tournament')
app.register_blueprint(root)
app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_cancel_duel, url_prefix='/cancel-duel')
app.register_blueprint(bp_console, url_prefix='/console')
app.register_blueprint(bp_console_admin, url_prefix='/admin/console')
app.register_blueprint(bp_convert, url_prefix='/convert-rate')
app.register_blueprint(bp_create_duel, url_prefix='/create-duel')
app.register_blueprint(bp_duel, url_prefix='/duel')
app.register_blueprint(bp_enter_duel, url_prefix='/enter-duel')
app.register_blueprint(bp_enter_team, url_prefix='/enter')
app.register_blueprint(bp_game, url_prefix='/game')
app.register_blueprint(bp_game_by_console, url_prefix='/game/console')
app.register_blueprint(bp_inform_invite_timeout,
                       url_prefix='/duel/inform-invite-timeout')

app.register_blueprint(bp_contact_email, url_prefix='/contact-email')
app.register_blueprint(bp_invitation_email, url_prefix='/invitation-email')
app.register_blueprint(bp_welcome_email, url_prefix='/welcome-email')
app.register_blueprint(bp_match_list, url_prefix='/match-list')
app.register_blueprint(bp_notification, url_prefix='/notification')
app.register_blueprint(bp_notification_read, url_prefix='/notification/set-as-read')
app.register_blueprint(bp_player, url_prefix='/player')
app.register_blueprint(bp_player_by_console, url_prefix='/player-by-game')
app.register_blueprint(bp_plan, url_prefix='/plan')
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_purchase, url_prefix='/purchase')
app.register_blueprint(bp_region_country, url_prefix='/region-country')
app.register_blueprint(bp_region_state, url_prefix='/region-state')
app.register_blueprint(bp_team, url_prefix='/team')
app.register_blueprint(bp_user_admin, url_prefix='/user-admin')
app.register_blueprint(bp_value, url_prefix='/values')
app.register_blueprint(bp_policy, url_prefix='/privacy-policy')
app.register_blueprint(bp_terms, url_prefix='/terms-and-conditions')


@app.route('/check', methods=['POST', 'GET'])
def index():
    return {
        'status': 'ok',
        'data': 'PlayerStars is alive!!'}


@app.lambda_function(name=Settings.DUEL_SCHEDULED_FINISHER_NAME)
def duel_finish_handler(event, context):
    return duel_scheduled_finisher(event['duel_id'])
