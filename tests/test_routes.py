#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from unittest.mock import MagicMock, patch
from app import index
from playerstars_routes.routes import home


# noinspection PyUnusedLocal
def test_get_root():
    result = index()

    assert result['status'] == 'ok'
    assert result['data'] == 'PlayerStars is alive!!'


def test_home():
    result = home()
    assert result == 'homezinha'
