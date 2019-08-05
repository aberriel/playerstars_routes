# -*- coding: utf-8 -*-

"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .console_route import ConsoleRoute
from .game_route import get_all_games, post_game
from .player_route import  player_registration
from .region_country_route import get_all_region_country, post_region_country, get_region_country
from .region_state_route import get_all_region_state, post_region_state, get_region_state
from .routes import root
