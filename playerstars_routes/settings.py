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
