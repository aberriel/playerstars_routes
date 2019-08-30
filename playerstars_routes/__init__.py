

"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .game_route import (
    delete_game,
    GameChaliceRoute,
    get_all_games,
    get_game_by_id,
    post_game,
    put_game,
)
from .player_route import (
    get_all_player,
    get_player_by_id,
    PlayerChaliceRoute,
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
from .team_route import (
    get_all_teams,
    get_all_teams_by_user,
    get_team_by_id,
    post_team,
    put_team,
    TeamChaliceRoute
)
from .user_admin_route import (
    get_all_user_admin,
    get_user_admin_by_id,
    post_user_admin,
    put_user_admin,
    UserAdminChaliceRoute
)
from .duel_route import (
    post_duel,
    get_match_list,
    MatchListChaliceRoute,
    enter_duel
)
from .basic_entity_route import BasicEntityRoute

__all__ = [
    'BasicEntityRoute',
    'UserAdminChaliceRoute',
    'GameChaliceRoute',
    'post_player',
    'post_game',
    'post_region_state',
    'post_region_country',
    'PlayerChaliceRoute',
    'get_all_player',
    'get_all_games',
    'get_game_by_id',
    'get_region_state_by_id',
    'get_all_region_state',
    'get_region_country_by_id',
    'get_all_region_country',
    'get_player_by_id',
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
    'TeamChaliceRoute',
    'post_duel',
    'get_match_list',
    'MatchListChaliceRoute',
    'enter_duel'
]
