from decouple import config


class Settings:
    LOG_LEVEL = config('LOG_LEVEL', 'DEBUG')

    CHAMPIONSHIP_TABLE_NAME = config(
        'CHAMPIONSHIP_TABLE_NAME', 'championship_dev')
    CONSOLE_TABLE_NAME = config('CONSOLE_TABLE_NAME', 'console_dev')
    CONVERT_STAR_TABLE_NAME = config(
        'CONVERT_STAR_TABLE_NAME', 'convert_rate_dev')
    DUEL_TABLE_NAME = config('DUEL_TABLE_NAME', 'duel_dev')
    NOTIFICATION_TABLE_NAME = config(
        'NOTIFICATION_TABLE_NAME', 'notification_dev')
    PLAYER_TABLE_NAME = config('PLAYER_TABLE_NAME', 'player_dev')
    PRODUCT_TABLE_NAME = config('PRODUCT_TABLE_NAME', 'product_dev')
    PURCHASE_HISTORY_TABLE_NAME = config(
        'PURCHASE_HISTORY_TABLE_NAME', 'purchase_dev')
    REGION_COUNTRY_TABLE_NAME = config(
        'REGION_COUNTRY_TABLE_NAME', 'region_country_dev')
    REGION_STATE_TABLE_NAME = config(
        'REGION_STATE_TABLE_NAME', 'region_state_dev')
    TEAM_TABLE_NAME = config('TEAM_TABLE_NAME', 'team_dev')
    USER_TABLE_NAME = config('USER_TABLE_NAME', 'user_dev')
    USER_ADMIN_TABLE_NAME = config('USER_ADMIN_TABLE_NAME', 'user_admin_dev')
    VALUES_TABLE_NAME = config('VALUES_TABLE_NAME', 'value_dev')

    CHAMPIONSHIP_MUTATION_NAME_PART = config(
        'CHAMPIONSHIP_MUTATION_NAME_PART', 'ChampionshipDev')
    DUEL_MUTATION_NAME_PART = config('DUEL_MUTATION_NAME_PART', 'DuelDev')
    NOTIFICATION_MUTATION_NAME_PART = config(
        'NOTIFICATION_MUTATION_NAME_PART',
        'NotificationDev')

    CHAMPIONSHIP_CHECK_TASK_NAME = config('CHAMPIONSHIP_CHECK_TASK_NAME',
                                          'championship_check_dev')

    AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION', 'us-east-1')
    CONTACT_EMAIL_RECIPIENTS = config(
        'CONTACT_EMAIL_RECIPIENTS',
        'noreply@stormsec.com.br')
    DUEL_SCHEDULED_FINISHER_NAME = config(
        'DUEL_SCHEDULED_FINISHER_NAME',
        'duel_scheduled_finisher_dev')
    DYNAMODB_URL = config('DYNAMODB_URL', None)
    PAGSEGURO_EMAIL = config('PAGSEGURO_EMAIL', 'wanderley@stormsec.com.br')
    PAGSEGURO_HOST_URL = config(
        'PAGSEGURO_HOST_URL',
        'https://ws.pagseguro.uol.com.br')
    PAGSEGURO_RETURN_URL = config('PAGSEGURO_RETURN_URL', 'www.google.com.br')
    PAGSEGURO_SANDBOX_ENABLE = config('PAGSEGURO_SANDBOX_ENABLE', True)
    PAGSEGURO_SANDBOX_HOST_URL = config(
        'PAGSEGURO_SANDBOX_HOST_URL',
        'https://ws.sandbox.pagseguro.uol.com.br')
    PAGSEGURO_SANDBOX_TOKEN = config(
        'PAGSEGURO_SANDBOX_TOKEN', '8D0B7247DE3B4F22ABBCCCE6AD802C19')
    PAGSEGURO_TOKEN = config(
        'PAGSEGURO_TOKEN', 'A0ABD34C342A474C8CEB112430FCCBD8')
    PAGSEGURO_UPDATE_NOTIFICATION_URL = config(
        'PAGSEGURO_UPDATE_NOTIFICATION_URL',
        '{host}/v3/transactions/notifications/{notification_code}'
        '?email={email}&token={token}')
    PLAYERSTARS_NOTIFICATION_URL = config(
        'PLAYERSTARS_NOTIFICATION_URL',
        'https://mb45dn63b2.execute-api.us-east-1.amazonaws.com'
        '/dev/purchase/notification')
    PURCHASE_OPERATION_TIMEOUT = config('PURCHASE_OPERATION_TIMEOUT', 20)
    RETURN_URL = config(
        'RETURN_URL',
        'http://playerstars-dev.s3-website-us-east-1.amazonaws.com')
    S3_BUCKET_NAME = config('S3_BUCKET_NAME', 'playerstars-dev-photos')
    S3_BUCKET_URL = config(
        'S3_BUCKET_URL',
        'http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com')
    GRAPHQL_API_URL = config(
        'GRAPHQL_API_URL',
        'https://c7zo7ax3oze6rk3gko45hnjcpy.appsync-'
        'api.us-east-1.amazonaws.com/graphql')
    GRAPHQL_API_ID = config('GRAPHQL_API_ID', '3l2u7ok2cjfwdclv5qz3zb5z54')
    GRAPHQL_API_KEY = config('GRAPHQL_API_KEY',
                             'da2-xqu7fukowrcilcwoxvcjsrfawm')
    TIME_TO_FINISH_DUEL = config('TIME_TO_FINISH_DUEL', 18000)
    RESULT_TIME = config('RESULT_TIME', 30000)
    RESPONSE_TIME = config('RESPONSE_TIME', 120)
