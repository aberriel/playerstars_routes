from decouple import config


class Settings:
    LOG_LEVEL = config('LOG_LEVEL', 'DEBUG')
    CONTACT_EMAIL_RECIPIENTS = config('CONTACT_EMAIL_RECIPIENTS',
                                      'noreply@stormsec.com.br')

    CHAMPIONSHIP_TABLE_NAME = config('CHAMPIONSHIP_TABLE_NAME',
                                     'championship')
    CONSOLE_TABLE_NAME = config('CONSOLE_TABLE_NAME', 'console')
    DUEL_TABLE_NAME = config('DUEL_TABLE_NAME', 'duel')
    NOTIFICATION_TABLE_NAME = config('NOTIFICATION_TABLE_NAME',
                                     'notification')
    PLAYER_TABLE_NAME = config('_TABPLAYERLE_NAME', 'player')
    PRODUCT_TABLE_NAME = config('PRODUCT_TABLE_NAME', 'product')
    PURCHASE_HISTORY_TABLE_NAME = config('_TABLE_NAMPURCHASE_HISTORYE',
                                         'purchase')
    REGION_COUNTRY_TABLE_NAME = config('REGION_COUNTRY_TABLE_NAME',
                                       'region_country')
    REGION_STATE_TABLE_NAME = config('REGION_STATE_TABLE_NAME',
                                     'region_state')
    TEAM_TABLE_NAME = config('TEAM_TABLE_NAME', 'team')
    USER_TABLE_NAME = config('USER_TABLE_NAME', 'user')
    USER_ADMIN_TABLE_NAME = config('USER_ADMIN_TABLE_NAME', 'user_admin')
    CONVERT_STAR_TABLE_NAME = config('CONVERT_STAR_TABLE_NAME', 'convert_rate')

    DYNAMODB_URL = config('DYNAMODB_URL', None)
    PURCHASE_OPERATION_TIMEOUT = config('PURCHASE_OPERATION_TIMEOUT', 20)
    PAGSEGURO_RETURN_URL = config('PAGSEGURO_RETURN_URL', 'www.google.com.br')
    PAGSEGURO_SANDBOX_ENABLE = config('PAGSEGURO_SANDBOX_ENABLE', True)
    PAGSEGURO_HOST_URL = config('PAGSEGURO_HOST_URL',
                                'https://ws.pagseguro.uol.com.br')
    PAGSEGURO_SANDBOX_HOST_URL = config(
        'PAGSEGURO_SANDBOX_HOST_URL',
        'https://ws.sandbox.pagseguro.uol.com.br')
    PAGSEGURO_EMAIL = config('PAGSEGURO_EMAIL', 'wanderley@stormsec.com.br')
    PAGSEGURO_TOKEN = config('PAGSEGURO_TOKEN',
                             'A0ABD34C342A474C8CEB112430FCCBD8')
    PAGSEGURO_SANDBOX_TOKEN = config('PAGSEGURO_SANDBOX_TOKEN',
                                     '8D0B7247DE3B4F22ABBCCCE6AD802C19')
    RETURN_URL = config(
        'RETURN_URL',
        'http://playerstars-dev.s3-website-us-east-1.amazonaws.com')
    PLAYERSTARS_NOTIFICATION_URL = config(
        'PLAYERSTARS_NOTIFICATION_URL',
        'https://mb45dn63b2.execute-api.us-east-1.amazonaws.com/dev/purchase'
        '/notification')
    PAGSEGURO_UPDATE_NOTIFICATION_URL = config(
        "PAGSEGURO_UPDATE_NOTIFICATION_URL",
        "{host}/v3/transactions/notifications/{notification_code}?email={"
        "email}&token={token}")
    S3_BUCKET_NAME = config("S3_BUCKET_NAME", "playerstars-dev-photos")
    S3_BUCKET_URL = config(
        "S#_BUCKET_URL",
        "http://playerstars-dev-photos.s3-website-us-east-1.amazonaws.com")

    DUEL_SCHEDULED_FINISHER_NAME = config(
        'DUEL_SCHEDULED_FINISHER_NAME',
        'PlayerStars-dev-duel_scheduled_finisher_dev')
    TIME_TO_FINISH_DUEL = config(
        'TIME_TO_FINISH_DUEL',
        18000)
    AWS_DEFAULT_REGION = config('AWS_DEFAULT_REGION', 'us-east-1')

    # "PAGSEGURO_NOTIFICATION_URL":
    # "https://t3hahl6qek.execute-api.us-east-1.amazonaws.com/api/pagseguro
    # /notificacao",
    # "PAGSEGURO_NOTIFICATIONS_URL": "https://ws.{
    # sandbox}pagseguro.uol.com.br/v3/transactions/notifications/{codigo}?{
    # credenciais}",
    # "PAGSEGURO_TRANSACTION_URL": "https://ws.{
    # sandbox}pagseguro.uol.com.br/v2/transactions"
