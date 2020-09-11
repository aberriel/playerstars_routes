from chalicelib.duel_scheduled_finisher import duel_scheduled_finisher
from unittest.mock import patch


@patch('chalicelib.duel_scheduled_finisher.DuelFinishHandler')
@patch('boto3.resource')
@patch('boto3.client')
def test_duel_scheduled_finisher(client, resource, duel_finish_handler):
    result = duel_scheduled_finisher('duel_id')
    assert result == \
        duel_finish_handler.return_value.duel_finish_handler.return_value
