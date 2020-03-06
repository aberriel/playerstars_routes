from chalicelib.settings import Settings
from os import path

import inspect
import json


config_file_path = '.chalice/config.json'


exclusion_list = ['AWS_DEFAULT_REGION', 'DYNAMODB_URL']


def read_config_json():
    with open(config_file_path) as json_file:
        data = json.load(json_file)
        return data


def get_settings_attribute_list():
    all_attributes = inspect.getmembers(
        Settings, lambda a:not(inspect.isroutine(a)))
    public_attributes = [a[0] for a in all_attributes
                         if not(a[0].startswith('__')
                                and a[0].endswith('__'))]
    return public_attributes


def get_settings_variables_table():
    config_from_settings = get_settings_attribute_list()
    found_table_configs = [x for x in config_from_settings
                           if 'TABLE_NAME' in x]
    return found_table_configs


def get_settings_variables_not_table():
    config_from_settings = get_settings_attribute_list()
    found_table_configs = [x for x in config_from_settings
                           if 'TABLE_NAME' not in x]
    return found_table_configs


def get_environment_variables_from_config():
    config_from_json = read_config_json()
    return config_from_json['environment_variables']


def get_stage_from_config(env):
    config_from_json = read_config_json()
    return config_from_json['stages'][env]


def test_config_file_exists():
    assert path.exists(config_file_path)
    assert path.isfile(config_file_path)


def test_check_has_stage_dev():
    config_from_json = read_config_json()
    assert 'dev' in config_from_json['stages']


def test_check_has_stage_stg():
    config_from_json = read_config_json()
    assert 'stg' in config_from_json['stages']


def test_check_has_stage_prd():
    config_content = read_config_json()
    assert 'prd' in config_content['stages']


def test_has_table_configs_on_environment_variables():
    tables = get_settings_variables_table()
    envs_part = get_environment_variables_from_config()
    for table in tables:
        assert table in envs_part
        assert '_dev' not in envs_part[table]
        assert '_stg' not in envs_part[table]
        assert '_prd' not in envs_part[table]


def test_has_environment_variables_on_environment_variables():
    envs = get_settings_variables_not_table()
    envs_part = get_environment_variables_from_config()
    for env in envs:
        if env not in exclusion_list:
            assert env in envs_part


def test_has_table_configs_on_dev():
    tables = get_settings_variables_table()
    stage_dev = get_stage_from_config('dev')
    environment_variables = stage_dev['environment_variables']
    for table in tables:
        assert table in environment_variables
        assert environment_variables[table]
        assert '_dev' in environment_variables[table]


def test_has_table_configs_on_stg():
    tables = get_settings_variables_table()
    stage_stg = get_stage_from_config('stg')
    environment_variables = stage_stg['environment_variables']
    for table in tables:
        assert table in environment_variables
        assert environment_variables[table]
        assert '_stg' in environment_variables[table]


def test_has_table_configs_on_prd():
    tables = get_settings_variables_table()
    stage_prd = get_stage_from_config('prd')
    for table in tables:
        assert table in stage_prd
        assert stage_prd[table]
        assert '_prd' in stage_prd[table]


def test_has_environment_variables_on_dev():
    envs = get_settings_variables_not_table()
    stage_dev = get_stage_from_config('dev')
    environment_variables = stage_dev['environment_variables']
    for env in envs:
        if env not in exclusion_list:
            assert env in environment_variables
            assert environment_variables[env]


def test_has_environment_variables_on_stg():
    tables = get_settings_variables_not_table()
    stage_dev = get_stage_from_config('stg')
    environment_variables = stage_dev['environment_variables']
    for env in tables:
        if env not in exclusion_list:
            assert env in environment_variables
            assert environment_variables[env]


def test_has_environment_variables_on_prd():
    tables = get_settings_variables_not_table()
    environment_variables = get_stage_from_config('prd')
    for env in tables:
        if env not in exclusion_list:
            assert env in environment_variables
            assert environment_variables[env]


def test_check_log_level():
    settings_envs = get_settings_variables_not_table()
    assert 'LOG_LEVEL' in settings_envs
    json_envs = get_environment_variables_from_config()
    assert 'LOG_LEVEL' in json_envs
    assert json_envs['LOG_LEVEL'] == 'INFO'


def test_check_log_level_dev():
    json_dev_envs = get_stage_from_config('dev')['environment_variables']
    assert 'LOG_LEVEL' in json_dev_envs
    assert json_dev_envs['LOG_LEVEL'] == 'DEBUG'


def test_check_log_level_stg():
    json_stg_envs = get_stage_from_config('stg')['environment_variables']
    assert 'LOG_LEVEL' in json_stg_envs
    assert json_stg_envs['LOG_LEVEL'] == 'DEBUG'


def test_check_log_level_prd():
    json_prd_envs = get_stage_from_config('prd')
    assert 'LOG_LEVEL' in json_prd_envs
    assert json_prd_envs['LOG_LEVEL'] == 'INFO'
