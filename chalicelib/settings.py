from decouple import config


class Settings:
    LOG_LEVEL = config('LOG_LEVEL', 'DEBUG')

    CONSOLE_TABLE_NAME = config('CONSOLE_TABLE_NAME', 'console')
    DUEL_TABLE_NAME = config('DUEL_TABLE_NAME', 'duel')
    PLAYER_TABLE_NAME = config('_TABPLAYERLE_NAME', 'player')
    PURCHASE_HISTORY_TABLE_NAME = config('_TABLE_NAMPURCHASE_HISTORYE',
                                         'purchase')
    REGION_COUNTRY_TABLE_NAME = config('REGION_COUNTRY_TABLE_NAME',
                                       'region_country')
    REGION_STATE_TABLE_NAME = config('REGION_STATE_TABLE_NAME', 'region_state')
    TEAM_TABLE_NAME = config('TEAM_TABLE_NAME', 'team')
    USER_TABLE_NAME = config('USER_TABLE_NAME', 'user')
    USER_ADMIN_TABLE_NAME = config('USER_ADMIN_TABLE_NAME', 'user_admin')
    DYNAMODB_URL = config('DYNAMODB_URL', None)
    PAGSEGURO_RETURN_URL = config('PAGSEGURO_RETURN_URL', 'www.google.com.br')
    PURCHASE_OPERATION_TIMEOUT = config('PURCHASE_OPERATION_TIMEOUT', 20)
    PAGSEGURO_SANDBOX_ENABLE = config('PAGSEGURO_SANDBOX_ENABLE', True)
    PAGSEGURO_EMAIL = config('PAGSEGURO_EMAIL', 'wanderley@stormsec.com.br')
    PAGSEGURO_TOKEN = config('PAGSEGURO_TOKEN', 'A0ABD34C342A474C8CEB112430FCCBD8')
    PAGSEGURO_SANDBOX_TOKEN = config('PAGSEGURO_SANDBOX_TOKEN', '8D0B7247DE3B4F22ABBCCCE6AD802C19')
    RETURN_URL = config('RETURN_URL', 'http://pagina-de-retorno-do-front')
    
    # "PAGSEGURO_NOTIFICATION_URL": "https://t3hahl6qek.execute-api.us-east-1.amazonaws.com/api/pagseguro/notificacao",
    # "PAGSEGURO_NOTIFICATIONS_URL": "https://ws.{sandbox}pagseguro.uol.com.br/v3/transactions/notifications/{codigo}?{credenciais}",
    # "PAGSEGURO_TRANSACTION_URL": "https://ws.{sandbox}pagseguro.uol.com.br/v2/transactions"
