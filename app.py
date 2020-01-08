from chalice import Chalice

from chalicelib import root
from chalicelib.championship_route import (
    bp_accept_invitation,
    bp_add_friend_to_championship,
    bp_championship,
    bp_join_open_championship
)
from chalicelib.console_route import bp_console
from chalicelib.duel_route import (
    bp_create_duel,
    bp_duel,
    bp_enter_duel,
    bp_match_list
)
from chalicelib.game_route import bp_game, bp_game_by_console
from chalicelib.notification_route import bp_notification
from chalicelib.player_route import bp_player
from chalicelib.product_route import bp_product
from chalicelib.purchase_route import bp_purchase
from chalicelib.region_country_route import bp_region_country
from chalicelib.region_state_route import bp_region_state
from chalicelib.send_contact_email import bp_contact_email
from chalicelib.send_invitation_email import bp_invitation_email
from chalicelib.send_welcome_email import bp_welcome_email
from chalicelib.team_route import (
    bp_team, bp_enter_team)
from chalicelib.user_admin_route import bp_user_admin
from chalicelib.convert_star_rate_route import bp_convert
from chalicelib.admin_routes import bp_admin

app = Chalice(app_name='playerstars')

app.experimental_feature_flags.update([
    'BLUEPRINTS'
])

app.register_blueprint(root, url_prefix='/')
app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(bp_console, url_prefix='/console')
app.register_blueprint(bp_contact_email, url_prefix='/contact-email')
app.register_blueprint(bp_game, url_prefix='/game')
app.register_blueprint(bp_game_by_console, url_prefix='/game/console')
app.register_blueprint(bp_invitation_email, url_prefix='/invitation-email')
app.register_blueprint(bp_match_list, url_prefix='/match-list')
app.register_blueprint(bp_notification, url_prefix='/notification')
app.register_blueprint(bp_player, url_prefix='/player')
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_purchase, url_prefix='/purchase')
app.register_blueprint(bp_region_country, url_prefix='/region-country')
app.register_blueprint(bp_region_state, url_prefix='/region-state')
app.register_blueprint(bp_team, url_prefix='/team')
app.register_blueprint(bp_user_admin, url_prefix='/user-admin')
app.register_blueprint(bp_welcome_email, url_prefix='/welcome-email')
app.register_blueprint(bp_create_duel, url_prefix='/create-duel')
app.register_blueprint(bp_duel, url_prefix='/duel')
app.register_blueprint(bp_enter_duel, url_prefix='/enter-duel')
app.register_blueprint(bp_enter_team, url_prefix='/enter')
app.register_blueprint(bp_convert, url_prefix='/convert-rate')
app.register_blueprint(bp_championship, url_prefix='/championship')


@app.route('/check', methods=['POST', 'GET'])
def index():
    return {'status': 'ok',
            'data': 'PlayerStars is alive!!'}
