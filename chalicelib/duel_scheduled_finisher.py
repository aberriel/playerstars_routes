from playerstars_aws_lambda import DuelFinishHandler
from chalicelib.settings import Settings


def duel_scheduled_finisher(duel_id):
    duel_finish_handler = DuelFinishHandler(duel_id,
                                            Settings.DUEL_TABLE_NAME,
                                            Settings.NOTIFICATION_TABLE_NAME,
                                            Settings.PLAYER_TABLE_NAME,
                                            Settings.DYNAMODB_URL)

    return duel_finish_handler.duel_finish_handler()
