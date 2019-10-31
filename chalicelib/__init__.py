from .basic_entity_route import BasicEntityRoute
from .championship_route import (
    post_accept_invitation,
    post_create_championship
)
from .duel_route import (
    post_duel,
    get_match_list,
    enter_duel,
    get_all_player_duels,
    get_all_duel,
    get_duels_by_status_route
)
from .game_route import (
    delete_game,
    get_all_games,
    get_game_by_id,
    post_game,
    put_game,
)
from .notification_route import (
    get_app_notification,
    post_app_notification
)
from .player_route import (
    get_all_player,
    get_player_by_id,
    post_player,
    put_player
)
from .product_route import get_all_product, post_product
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
from .send_contact_email import post_contact_email
from .send_invitation_email import post_invitation_email
from .send_welcome_email import post_welcome_email
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
    'get_all_player_duels',
    'get_all_duel',
    'get_duels_by_status_route',

    'get_all_product',
    'post_product',

    'post_contact_email',
    'post_invitation_email',
    'post_welcome_email',

    'post_app_notification',
    'get_app_notification',

    'post_accept_invitation',
    'post_create_championship'
]
