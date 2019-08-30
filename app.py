from chalice import Chalice

from playerstars_routes import root
from playerstars_routes.console_route import bp_console
from playerstars_routes.game_route import bp_game
from playerstars_routes.player_route import bp_player
from playerstars_routes.region_country_route import bp_region_country
from playerstars_routes.region_state_route import bp_region_state
from playerstars_routes.user_admin_route import bp_user_admin
from playerstars_routes.duel_route import (
    bp_match_list, bp_create_duel, bp_enter_duel)

app = Chalice(app_name='playerstars')

app.experimental_feature_flags.update([
    'BLUEPRINTS'
])

app.register_blueprint(root, url_prefix='/')
app.register_blueprint(bp_console, url_prefix='/console')
app.register_blueprint(bp_user_admin, url_prefix='/user-admin')
app.register_blueprint(bp_game, url_prefix='/game')
app.register_blueprint(bp_player, url_prefix='/')
app.register_blueprint(bp_region_country, url_prefix='/region-country')
app.register_blueprint(bp_region_state, url_prefix='/region-state')
app.register_blueprint(bp_match_list, url_prefix='/match-list')
app.register_blueprint(bp_create_duel, url_prefix='/create-duel')
app.register_blueprint(bp_enter_duel, url_prefix='/enter-duel')


@app.route('/check', methods=['POST', 'GET'])
def index():
    return {'status': 'ok',
            'data': 'PlayerStars is alive!!'}
