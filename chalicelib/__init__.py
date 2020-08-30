from .admin_routes import (
    get_all_players_admin,
    get_player_by_id_admin,
    put_player_admin,
    post_console_admin,
    put_console_admin,
    delete_console_admin,
    get_all_duel_admin,
    get_duel_by_id_admin,
    get_all_terms_admin,
    get_terms_by_id_admin,
    post_terms_admin,
    put_terms_admin,
    delete_terms_admin,
    get_privacy_by_id_admin,
    get_all_privacy_admin,
    post_privacy_admin,
    put_privacy_admin,
    delete_privacy_admin)
from .basic_entity_route import BasicEntityRoute

# from .championship_route import (
#     get_all_championships,
#     get_championship_by_id,
#     get_championships_by_player,
#     get_championships_by_team,
#     get_open_championships,
#     post_accept_invitation,
#     post_add_friend_to_championship,
#     post_create_championship,
#     post_join_open_championship)

from .console_route import (
    post_console,
    put_console
)
from .convert_star_rate_route import (
    delete_convert_rate, get_all_convert_rate, get_convert_rate_by_id,
    put_convert_rate, post_convert_rate
)
from .duel_route import (
    cancel_duel_route,
    end_duel,
    enter_duel,
    get_all_duel,
    get_all_player_duels,
    get_duel,
    get_duels_by_status_route,
    get_match_list,
    get_opponent_list_route,
    inform_invitation_timeout,
    post_duel,
    reject_duel_route,
    get_duel_details,
    get_opponent_teams_for_duel,
    get_random_duel,
    put_random_duel,
    delete_random_duel,
    post_random_duel
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
    get_app_notification_by_status,
    post_app_notification,
    post_set_notification_as_read)
from .player_route import (
    get_all_player,
    get_player_by_id,
    post_player,
    put_player,
    post_accept_terms_route,
    post_console_data_route,
    get_all_player_by_console,
    convert_star_route,
    get_player_consoles,
    get_friends_by_console_game_route,
    get_accepted_teams_from_player,
    get_my_teams_for_duel,
    get_ranking_my_teams_route,
    get_player_tournaments
)
from .product_route import get_all_plan, get_all_product, post_product
from .pagseguro_purchase_route import (
    get_history_route
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
from .mail_routes import (
    post_contact_email,
    post_invitation_email,
    post_welcome_email,
    post_public_contact_email
)
from .team_route import (
    accept_invitation,
    delete_team,
    get_all_teams,
    get_all_teams_by_user,
    get_team_by_id,
    leave_team,
    post_team,
    put_team,
    enter_team
)
from .user_admin_route import (
    get_all_user_admin,
    get_user_admin_by_id,
    post_user_admin,
    put_user_admin
)
from .values_route import (
    get_all_values,
    get_value_by_id,
    post_value,
    put_value,
    delete_value
)
from .terms_policy_route import (
    get_policy,
    get_terms
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
    'enter_team',
    'delete_team',
    'leave_team',
    'accept_invitation',

    'get_all_plan',
    'get_all_product',
    'post_product',

    'post_contact_email',
    'post_invitation_email',
    'post_welcome_email',
    'post_public_contact_email',

    'get_app_notification_by_status',
    'get_app_notification',
    'post_app_notification',
    'post_set_notification_as_read',

    'get_history_route',

    'get_all_player_by_console',

    'get_convert_rate_by_id',
    'get_all_convert_rate',
    'post_convert_rate',
    'put_convert_rate',
    'delete_convert_rate',

    'convert_star_route',

    'get_all_players_admin',
    'get_player_by_id_admin',
    'put_player_admin',

    'cancel_duel_route',
    'end_duel',
    'enter_duel',
    'get_all_duel',
    'get_all_player_duels',
    'get_duel',
    'get_duels_by_status_route',
    'get_match_list',
    'get_opponent_list_route',
    'inform_invitation_timeout',
    'post_duel',
    'reject_duel_route',

    'put_player',
    'post_accept_terms_route',
    'post_console_data_route',

    'post_console',
    'put_console',

    'post_console_admin',
    'put_console_admin',
    'delete_console_admin',

    'get_player_consoles',

    'get_value_by_id',
    'get_all_values',
    'put_value',
    'post_value',
    'delete_value',

    'get_friends_by_console_game_route',

    'get_duel_details',

    'get_accepted_teams_from_player',

    'get_opponent_teams_for_duel',
    'get_my_teams_for_duel',
    'get_all_duel_admin',
    'get_duel_by_id_admin',
    'get_terms_by_id_admin',
    'get_all_terms_admin',
    'post_terms_admin',
    'put_terms_admin',
    'delete_terms_admin',
    'get_all_privacy_admin',
    'get_privacy_by_id_admin',
    'post_privacy_admin',
    'put_privacy_admin',
    'delete_privacy_admin',

    'get_policy',
    'get_terms',

    'get_ranking_my_teams_route',

    'get_random_duel',
    'put_random_duel',
    'delete_random_duel',
    'post_random_duel',

    'get_player_tournaments'
]
