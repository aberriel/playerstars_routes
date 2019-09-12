#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chalicelib import (
    get_all_star_transactions,
    get_filter_param,
    mount_get_request_model
)
from datetime import datetime, timezone
from enum import Enum
from playerstars_domain import (
    CoinType,
    OperationType,
    SourceOperationType
)
from playerstars_interactors import (
    GetStarTransactionHistoryException,
    GetStarTransactionHistoryRequestModel
)
from unittest.mock import MagicMock, patch

import json


def make_filters():
    payload = """{
        "coin": "BLUE_STAR",
        "operation_type": "DEBIT"
    }"""
    data = json.loads(payload)
    return MagicMock(current_request=MagicMock(json_body=data))


class PersonType(Enum):
    PESSOA_FISICA = 'PessoaFisica'
    PESSOA_JURIDICA = 'PessoaJuridica'


def make_filter_mock():
    return {
        'name': 'Anselmo Lira',
        'age': 32,
        'creation_date': '2019-02-13T12:25:33+00:00',
        'person_type': 'PessoaFisica',
        'address': None
    }


def test_get_filter_param():
    # Testando pegar String
    filter_param_1 = get_filter_param(make_filter_mock(), 'name', str)
    assert filter_param_1 == 'Anselmo Lira'

    # Testando pegar inteiro
    filter_param_2 = get_filter_param(make_filter_mock(), 'age', int)
    assert filter_param_2
    assert filter_param_2 == 32

    # Testando pegar enum
    filter_param_3 = get_filter_param(make_filter_mock(),
                                      'person_type',
                                      PersonType)
    assert filter_param_3
    assert filter_param_3 == PersonType.PESSOA_FISICA

    # Testando pegar datetime
    filter_param_4 = get_filter_param(make_filter_mock(),
                                      'creation_date',
                                      datetime)
    assert filter_param_4 == datetime(2019, 2, 13, 12, 25, 33,
                                      tzinfo=timezone.utc)

    # Tentando pegar sem fornecer o tipo
    filter_param_5 = get_filter_param(make_filter_mock(), 'creation_date')
    assert filter_param_5 == '2019-02-13T12:25:33+00:00'

    # Testando pegar ítem que não existe
    filter_param_6 = get_filter_param(make_filter_mock(), 'salary')
    assert not filter_param_6

    # Testando pegar ítem nulo
    filter_param_7 = get_filter_param(make_filter_mock(), 'address')
    assert not filter_param_7


def test_mount_request_model():
    filters_1 = {
        'coin_type': 'BLUE_STAR',
        'operation_type': 'CREDIT'
    }
    filters_2 = {
        'source_type': 'DUEL',
        'minimum_datetime': '2019-02-13T12:25:33+00:00',
        'maximum_datetime': '2019-06-11T23:45:55+00:00'
    }

    request_1 = mount_get_request_model(filters_1, '123')
    request_compare_1 = GetStarTransactionHistoryRequestModel(
        player_id='123',
        coin_type=CoinType.BLUE_STAR,
        operation_type=OperationType.CREDIT
    )

    assert request_1.player_id == request_compare_1.player_id
    assert request_1.coin_type == request_compare_1.coin_type
    assert request_1.source_type == request_compare_1.source_type
    assert request_1.maximum_datetime == request_compare_1.maximum_datetime
    assert request_1.minimum_datetime == request_compare_1.minimum_datetime
    assert request_1.operation_type == request_compare_1.operation_type

    request_2 = mount_get_request_model(filters_2, '456')
    request_compare_2 = GetStarTransactionHistoryRequestModel(
        player_id='456',
        source_type=SourceOperationType.DUEL,
        minimum_datetime=datetime(2019, 2, 13, 12, 25, 33,
                                  tzinfo=timezone.utc),
        maximum_datetime=datetime(2019, 6, 11, 23, 45, 55,
                                  tzinfo=timezone.utc)
    )

    assert request_2.player_id == request_compare_2.player_id
    assert request_2.coin_type == request_compare_2.coin_type
    assert request_2.source_type == request_compare_2.source_type
    assert request_2.maximum_datetime == request_compare_2.maximum_datetime
    assert request_2.minimum_datetime == request_compare_2.minimum_datetime
    assert request_2.operation_type == request_compare_2.operation_type


# noinspection PyUnusedLocal
@patch('chalicelib.star_transactions_route.bp_transactions', make_filters())
@patch('chalicelib.star_transactions_route.'
       'GetStarTransactionHistoryInteractor.run')
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_star_transactions(client, resource, run):
    result = get_all_star_transactions('123')
    run.assert_called_once()
    assert result.body['status'] == 'success'
    assert result.status_code == 200


# noinspection PyUnusedLocal
@patch('chalicelib.star_transactions_route.bp_transactions', make_filters())
@patch('chalicelib.star_transactions_route.'
       'GetStarTransactionHistoryInteractor.run',
       MagicMock(return_value=None))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_star_transactions_not_found(client, resource):
    result = get_all_star_transactions('123')
    assert result.body['message'] == 'Nenhuma transação encontrada'
    assert result.body['status'] == 'error'
    assert result.status_code == 404


# noinspection PyUnusedLocal
@patch('chalicelib.star_transactions_route.bp_transactions', make_filters())
@patch('chalicelib.star_transactions_route.'
       'GetStarTransactionHistoryInteractor.run',
       MagicMock(side_effect=GetStarTransactionHistoryException('oops')))
@patch('boto3.resource')
@patch('boto3.client')
def test_get_all_star_transactions_raises(client, resource):
    result = get_all_star_transactions('123')
    assert result.body['message'] == 'oops'
    assert result.body['status'] == 'error'
    assert result.status_code == 500
