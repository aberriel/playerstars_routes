from chalicelib.settings import Settings
from os import path

import inspect
import json
import os


config_file_path = '.chalice/config.json'


exclusion_list = ['AWS_DEFAULT_REGION']


def get_config_from_json():
    with open(config_file_path) as json_file:
        data = json.load(json_file)
        return data


def get_settings_attribute_list():
    all_attributes = inspect.getmembers(Settings, lambda a:not(inspect.isroutine(a)))
    public_attributes = [a[0] for a in all_attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
    return public_attributes


def get_settings_variables_table():
    all_attributes = get_settings_attribute_list()
    found_table_configs = [x for x in all_attributes if 'TABLE_NAME' in x]
    return found_table_configs


def get_settings_variables_not_table():
    all_attributes = get_settings_attribute_list()
    found_table_configs = [x for x in all_attributes if 'TABLE_NAME' not in x]
    return found_table_configs


def get_environment_variables_from_config():
    config_content = get_config_from_json()
    return config_content['environment_variables']


def get_stage_from_config(env):
    config_content = get_config_from_json()
    return config_content['stages'][env]


def test_config_file_exists():
    assert path.exists(config_file_path)
    assert path.isfile(config_file_path)


def test_check_has_stage_dev():
    config_content = get_config_from_json()
    assert 'dev' in config_content['stages']


def test_check_has_stage_stg():
    config_content = get_config_from_json()
    assert 'stg' in config_content['stages']


def test_check_has_stage_prd():
    config_content = get_config_from_json()
    assert 'prd' in config_content['stages']


def test_has_table_configs_on_dev():
    tables = get_settings_variables_table()
    stage_dev = get_stage_from_config('dev')
    environment_variables = stage_dev['environment_variables']
    assert(all(table in environment_variables for table in tables))


def test_has_table_configs_on_stg():
    tables = get_settings_variables_table()
    stage_dev = get_stage_from_config('stg')
    environment_variables = stage_dev['environment_variables']
    assert(all(table in environment_variables for table in tables))


def test_has_table_configs_on_prd():
    tables = get_settings_variables_table()
    environment_variables = get_stage_from_config('prd')
    assert(all(table in environment_variables for table in tables))


def test_has_environment_variables_on_dev():
    envs = get_settings_variables_not_table()
    stage_dev = get_stage_from_config('dev')
    environment_variables = stage_dev['environment_variables']
    for env in envs:
        if env not in exclusion_list:
            assert env in environment_variables


def test_has_environment_variables_on_stg():
    tables = get_settings_variables_not_table()
    stage_dev = get_stage_from_config('stg')
    environment_variables = stage_dev['environment_variables']
    for env in tables:
        if env not in exclusion_list:
            assert env in environment_variables


def test_has_environment_variables_on_prd():
    tables = get_settings_variables_not_table()
    environment_variables = get_stage_from_config('prd')
    for env in tables:
        if env not in exclusion_list:
            assert env in environment_variables
