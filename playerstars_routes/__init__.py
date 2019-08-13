# -*- coding: utf-8 -*-

"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .console_route import ConsoleRoute, post_console, put_console, \
    get_all_console, get_console_by_id, delete_console
from .game_route import get_all_games, post_game, GameRoute
from .player_route import PlayerRoute, post_player, get_player_by_id, \
    get_all_player
from .region_country_route import get_all_region_country, \
    post_region_country, get_region_country_by_id, RegionCountryRoute, \
    put_region_country
from .region_state_route import get_all_region_state, post_region_state, \
    get_region_state_by_id, RegionStateRoute, put_region_state
from .routes import root

__all__ = ['ConsoleRoute',
           'RegionStateRoute',
           'RegionCountryRoute',
           'GameRoute',
           'post_player',
           'post_game',
           'post_region_state',
           'post_console',
           'post_region_country',
           'PlayerRoute',
           'get_all_player',
           'get_all_games',
           'get_region_state_by_id',
           'get_all_region_state',
           'get_region_country_by_id',
           'get_all_region_country',
           'get_all_console',
           'get_console_by_id',
           'get_player_by_id',
           'put_console',
           'delete_console',
           'root',
           'put_region_country',
           'put_region_state']
