from unittest.mock import patch

from chalicelib.duel_scheduled_finisher import duel_scheduled_finisher


@patch('chalicelib.duel_scheduled_finisher.DuelFinishHandler')
def test_duel_scheduled_finisher(mock):
    result = duel_scheduled_finisher('um id qualquer')
    assert result == mock.return_value.duel_finish_handler.return_value
