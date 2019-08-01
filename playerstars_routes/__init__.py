# -*- coding: utf-8 -*-

"""Top-level package for PlayerStars Adapters."""

__author__ = """Storm Development Ltda"""
__email__ = 'playerstars@stormsec.com.br'
__version__ = '0.1.0'

from .routes import root
from .game_route import get_all_games, post_game
from .region_country_route import get_all_region_country, post_region_country
from .console_route import get_all_consoles, get_console, post_console

