from chalicelib.settings import Settings
from playerstars_adapters import DuelAdapter, PlayerAdapter, TeamAdapter
from playerstars_aws_lambda import DuelFinishHandler
from playerstars_graphql_adapters import NotificationAdapter


def get_duel_adapter():
    return DuelAdapter(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)


def get_notification_adapter():
    return NotificationAdapter(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.NOTIFICATION_MUTATION_NAME_PART)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME, Settings.DYNAMODB_URL)


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


def duel_scheduled_finisher(duel_id):
    duel_finish_handler = DuelFinishHandler(
        duel_id=duel_id,
        duel_adapter=get_duel_adapter(),
        notification_adapter=get_notification_adapter(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter())
    return duel_finish_handler.duel_finish_handler()
