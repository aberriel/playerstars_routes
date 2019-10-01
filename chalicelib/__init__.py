

"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .basic_entity_route import BasicEntityRoute
from .duel_route import (
    post_duel,
    get_match_list,
    enter_duel
)
from .game_route import (
    delete_game,
    get_all_games,
    get_game_by_id,
    post_game,
    put_game,
)
from .player_route import (
    get_all_player,
    get_player_by_id,
    post_player,
)
from .region_country_route import (
    get_all_region_country,
    get_region_country_by_id,
    post_region_country,
    put_region_country
)
from .region_state_route import (
    get_all_region_state,
    get_region_state_by_id,
    post_region_state,
    put_region_state
)
from .routes import root
from .star_transactions_route import (
    get_all_star_transactions,
    get_filter_param,
    mount_get_request_model
)
from .team_route import (
    get_all_teams,
    get_all_teams_by_user,
    get_team_by_id,
    post_team,
    put_team
)
from .user_admin_route import (
    get_all_user_admin,
    get_user_admin_by_id,
    post_user_admin,
    put_user_admin
)
from .product_route import get_all_product

__all__ = [
    'BasicEntityRoute',
    'post_game',
    'post_region_state',
    'post_region_country',
    'post_player',
    'get_all_player',
    'get_player_by_id',
    'get_all_games',
    'get_game_by_id',
    'get_region_state_by_id',
    'get_all_region_state',
    'get_region_country_by_id',
    'get_all_region_country',
    'root',
    'put_region_country',
    'put_region_state',
    'post_user_admin',
    'get_all_user_admin',
    'get_user_admin_by_id',
    'put_user_admin',
    'delete_game',
    'put_game',
    'get_all_teams',
    'get_all_teams_by_user',
    'get_team_by_id',
    'post_team',
    'put_team',
    'post_duel',
    'get_match_list',
    'enter_duel',

    'get_all_star_transactions',
    'get_filter_param',
    'mount_get_request_model',

    'get_all_product'
]
