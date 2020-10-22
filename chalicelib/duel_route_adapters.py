from playerstars_adapters import PreDuelAdapter, \
    DuelAdapter as DuelAdapterDynamo, ConsoleAdapter, \
    NotificationAdapter as NotificationAdapterDynamo, PlayerAdapter, \
    TeamAdapter
from playerstars_aws_scheduled_task_adapter import AwsScheduleTaskAdapter
from playerstars_graphql_adapters import DuelAdapter as DuelAdapterGraphql, \
    NotificationAdapter as NotificationAdapterGraphql
from playerstars_adapters import EventReminderAssistantAdapter
from aws_task_scheduler import AwsTaskSchedulerAdapter
from chalicelib.settings import Settings


def get_preduel_adapter():
    return PreDuelAdapter(Settings.PREDUEL_TABLE_NAME, Settings.DYNAMODB_URL)


def get_duel_adapter_dynamo():
    return DuelAdapterDynamo(Settings.DUEL_TABLE_NAME,
                             Settings.DYNAMODB_URL)


def get_console_adapter():
    return ConsoleAdapter(Settings.CONSOLE_TABLE_NAME, Settings.DYNAMODB_URL)


def get_duel_adapter_graphql():
    return DuelAdapterGraphql(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.DUEL_MUTATION_NAME_PART)


def get_notification_adapter_dynamo():
    return NotificationAdapterDynamo(Settings.NOTIFICATION_TABLE_NAME,
                                     Settings.DYNAMODB_URL)


def get_notification_adapter_graphql():
    return NotificationAdapterGraphql(
        api_id=Settings.GRAPHQL_API_ID,
        api_key=Settings.GRAPHQL_API_KEY,
        aws_region=Settings.AWS_DEFAULT_REGION,
        object_name=Settings.NOTIFICATION_MUTATION_NAME_PART)


def get_player_adapter():
    return PlayerAdapter(Settings.PLAYER_TABLE_NAME,
                         Settings.DYNAMODB_URL)


def get_team_adapter():
    return TeamAdapter(Settings.TEAM_TABLE_NAME, Settings.DYNAMODB_URL)


def get_schedule_task_adapter():
    schedule_task_adapter = AwsScheduleTaskAdapter(
        name='duel-finish',
        task_identifier=Settings.DUEL_SCHEDULED_FINISHER_NAME,
        aws_region=Settings.AWS_DEFAULT_REGION)
    return schedule_task_adapter


def get_era_adapter():
    era_adapter = EventReminderAssistantAdapter(
        table_name=Settings.ERA_TABLE_NAME
    )
    return era_adapter


def get_aws_task_scheduler_adapter():
    aws_task_scheduler_adapter = AwsTaskSchedulerAdapter(
        name='duel-finisher',
        lambda_runner=f'{Settings.ERA_AWS_LAMBDA_FUNCTION_NAME}-'
        f'{Settings.ERA_FINISH_DUEL_URL}'
    )
    return aws_task_scheduler_adapter
