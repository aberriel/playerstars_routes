from chalicelib.settings import Settings
from playerstars_adapters import (
    DuelAdapter as DuelAdapterDynamo,
    PlayerAdapter, ValuesAdapter,
    TeamAdapter)
from playerstars_aws_lambda import DuelFinishHandler, DuelFinishHandlerAdapters
from playerstars_graphql_adapters import (
    DuelAdapter as DuelAdapterGraphql,
    NotificationAdapter)
from chalicelib.aspect.logging import logger_aspect


def get_duel_adapter_dynamo():
    return DuelAdapterDynamo(Settings.DUEL_TABLE_NAME, Settings.DYNAMODB_URL)


def get_duel_adapter_graphql():
    return DuelAdapterGraphql(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.DUEL_MUTATION_NAME_PART)


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


def get_values_adapter():
    return ValuesAdapter(Settings.VALUES_TABLE_NAME, Settings.DYNAMODB_URL)


@logger_aspect
def duel_scheduled_finisher(duel_id):
    adapters = DuelFinishHandlerAdapters(
        duel_adapter_dynamo=get_duel_adapter_dynamo(),
        duel_adapter_graphql=get_duel_adapter_graphql(),
        notification_adapter=get_notification_adapter(),
        player_adapter=get_player_adapter(),
        team_adapter=get_team_adapter(),
        values_adapter=get_values_adapter()
    )
    duel_finish_handler = DuelFinishHandler(
        duel_id=duel_id,
        adapters=adapters,
        duel_judge_matrix=Settings.DUEL_JUDGE_MATRIX)
    return duel_finish_handler.duel_finish_handler()
