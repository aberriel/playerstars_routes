from chalice import Chalice

from chalicelib import root
from chalicelib.console_route import bp_console
from chalicelib.game_route import bp_game, bp_game_by_console
from chalicelib.player_route import bp_player
from chalicelib.region_country_route import bp_region_country
from chalicelib.region_state_route import bp_region_state
from chalicelib.user_admin_route import bp_user_admin
from chalicelib.team_route import bp_team
from chalicelib.duel_route import (
    bp_match_list, bp_create_duel, bp_enter_duel)
from chalicelib.send_email import bp_email
from chalicelib.purchase_route import bp_purchase

app = Chalice(app_name='playerstars')

app.experimental_feature_flags.update([
    'BLUEPRINTS'
])

app.register_blueprint(root, url_prefix='/')
app.register_blueprint(bp_console, url_prefix='/console')
app.register_blueprint(bp_user_admin, url_prefix='/user-admin')
app.register_blueprint(bp_game, url_prefix='/game')
app.register_blueprint(bp_game_by_console, url_prefix='/game/console')
app.register_blueprint(bp_player, url_prefix='/player')
app.register_blueprint(bp_region_country, url_prefix='/region-country')
app.register_blueprint(bp_region_state, url_prefix='/region-state')
app.register_blueprint(bp_match_list, url_prefix='/match-list')
app.register_blueprint(bp_create_duel, url_prefix='/create-duel')
app.register_blueprint(bp_enter_duel, url_prefix='/enter-duel')
app.register_blueprint(bp_team, url_prefix='/team')
app.register_blueprint(bp_email, url_prefix='/email')
app.register_blueprint(bp_purchase, url_prefix='/purchase')


@app.route('/check', methods=['POST', 'GET'])
def index():
    return {'status': 'ok',
            'data': 'PlayerStars is alive!!'}
