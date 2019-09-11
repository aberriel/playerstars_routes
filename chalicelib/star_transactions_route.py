#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chalice import Blueprint
from chalicelib.settings import Settings
from chalicelib.chalice_support.api_responses import (success,
                                                      not_found,
                                                      server_error,
                                                      created)
from datetime import datetime
from enum import EnumMeta
from playerstars_adapters import (
    DuelAdapter,
    PlayerAdapter
)
from playerstars_domain import (
    CoinType,
    OperationType,
    Player,
    PlayerStatus,
    SourceOperationType
)
from playerstars_interactors import (
    GetStarTransactionHistoryException,
    GetStarTransactionHistoryInteractor,
    GetStarTransactionHistoryRequestModel,
    GetStarTransactionHistoryResponseModel
)

import json


bp_transactions = Blueprint(__name__)


def get_filter_param(filters, parameter_name, parameter_type=None):
    if parameter_name in filters and filters[parameter_name]:
        if parameter_type and isinstance(parameter_type, EnumMeta):
            return parameter_type(filters[parameter_name])
        elif parameter_type and parameter_type == datetime:
            return datetime.fromisoformat(filters[parameter_name])
        else:
            return filters[parameter_name]
    return None


def mount_get_request_model(filters, player_id):
    request_model = GetStarTransactionHistoryRequestModel(
        player_id=player_id,
        coin_type=get_filter_param(filters, 'coin_type', CoinType),
        operation_type=get_filter_param(filters, 'operation_type', OperationType),
        source_type=get_filter_param(filters, 'source_type', SourceOperationType),
        minimum_datetime=get_filter_param(filters, 'minimum_datetime', datetime),
        maximum_datetime=get_filter_param(filters, 'maximum_datetime', datetime)
    )
    return request_model


@bp_transactions.route('/{player_id}')
def get_all_star_transactions(player_id):
    filters = bp_transactions.current_request.json_body
    duel_adapter = DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)
    player_adapter = PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)

    try:
        request = mount_get_request_model(filters, player_id)
        interactor = GetStarTransactionHistoryInteractor(
            request=request,
            player_adapter=player_adapter,
            duel_adapter=duel_adapter
        )
        response = interactor.run()

        if response:
            return success(response)

        return not_found('Nenhuma transação encontrada')
    except GetStarTransactionHistoryException as exc:
        return server_error(str(exc))
