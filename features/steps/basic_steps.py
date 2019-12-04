from app import app
from behave import *
import json
from chalicelib.settings import Settings
from playerstars_adapters import (
    ConsoleAdapter, CountryRegionAdapter, ChampionshipAdapter,
    StateRegionAdapter, UserAdminAdapter, NotificationAdapter,
    PlayerAdapter)
from tests.test_utils import jwt
import jsondiff


class Object(object):
    pass


convert_string_to_adapter = {
    'championship': ChampionshipAdapter,
    'console': ConsoleAdapter,
    'notification': NotificationAdapter,
    'region_country': CountryRegionAdapter,
    'region_state': StateRegionAdapter,
    'user_admin': UserAdminAdapter,
    'player': PlayerAdapter
}


def saved(context):
    found = False
    adapter = context.adapter(context.table_name, context.dynamo_url)

    for item in adapter.list_all():
        if context.saved_entity_id == item.entity_id:
            found = True
    return True if found else False


@given('I set table name and the adapter class as {table_name}')
def json_body(context, table_name):
    context.table_name = table_name.lower()
    context.adapter = convert_string_to_adapter[context.table_name]


@given('I save a new entry to the database with json body')
def save_new_entry(context):
    body = context.text
    context.json_body = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)
    context.saved_entity_id = adapter.save(context.json_body)
    assert saved(context)


@given('I emptied the database')
def data_base_is_empty(context):
    adapter = context.adapter(context.table_name, context.dynamo_url)

    get_all_consoles = adapter.list_all
    if get_all_consoles():
        for item in get_all_consoles():
            adapter.delete(item.entity_id)
    database_after_delete = get_all_consoles()
    assert database_after_delete == []


@given('I set {env} as {value}')
def set_env_var(context, env, value):
    Settings.DYNAMODB_URL = str(value)
    context.dynamo_url = Settings.DYNAMODB_URL


@when('{method} request is made to {url}')
def json_request(context, method, url):
    if 'json_body' in context:
        app.current_request = Object()
        app.current_request.query_params = None
        app.current_request.json_body = context.json_body
        app.current_request.headers = dict(AUTHORIZATION=jwt)
    url_method = app.routes.get(url)[method.upper()]
    response = url_method.view_function()
    # response = app.routes.get(url)[method.upper()].view_function().body
    context.response = response
    if method.upper() == 'GET':
        context.dict_list_get_all = context.response.body['data']
    context.item_id = context.response.body['data']
    try:
        context.response.json = json.loads(context.response)
    except Exception:
        pass


@when('{method} request is made with id {entity_id} to {url}')
def json_request_with_id(context, method, entity_id, url):
    if 'json_body' in context:
        app.current_request = Object()
        app.current_request.query_params = None
        app.current_request.json_body = context.json_body
        app.current_request.headers = dict(AUTHORIZATION=jwt)
    url_method = app.routes.get(url+"/{entity_id}")[method.upper()]
    response = url_method.view_function(entity_id)
    context.response = response
    if method.upper() in ['GET']:
        if url == '/game/console' and isinstance(context.response.body['data'], list):
            context.list_get_game = context.response.body['data']
        else:
            context.item_id = context.response.body['data']['entity_id']
    else:
        context.item_id = context.response.body['data']
    try:
        context.response.json = json.loads(context.response)
    except Exception:
        pass


@then('The response should have status {status}')
def json_response_status(context, status):
    assert context.response.body['status'] == status


@then('The response should have status_code {status_code}')
def json_response_status_code(context, status_code):
    print(context.response.status_code)
    assert context.response.status_code == int(status_code)


@given('The request has json body')
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@then('The follow notification is saved in the database')
def check_championship_notifications(context):
    body = context.text
    context.expected_json = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)
    response = adapter.list_all()
    notification = get_notification_by_player_id(
        response, context.expected_json['player_id'])
    print("NOTIFICATION: ", notification.to_json())
    res = jsondiff.diff(context.expected_json, notification.to_json())
    print(res)
    assert check_ignored_list(res)


def get_notification_by_player_id(response, playerd_id):
    for x in response:
        if x.player_id == playerd_id:
            return x


@then('The saved championship has body')
def check_keys(context):
    body = context.text
    context.expected_json = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)
    response = adapter.get_by_id(context.item_id).to_json()
    res = jsondiff.diff(context.expected_json, response)
    context.invited_players_id_list = get_invited_players_ids(response)
    assert check_ignored_list(res)


def get_invited_players_ids(response):
    invited_players_id_list = list()
    for x in response['members']:
        if x['member_category'] == 'member':
            invited_players_id_list.append(x['member'])
    return invited_players_id_list


def check_ignored_list(a):
    ignored_keys_list = [
        'last_status_change_date', 'invitation_code', 'entity_id',
        'start_datetime', 'creation_datetime', 'championship_id']
    for key, value in a.items():
        if isinstance(value, str) or isinstance(value, int):
            if key not in ignored_keys_list:
                print("KEY ACHADA QUE NAO EXISTE: ", key)
                return False
        if isinstance(value, dict):
            check_ignored_list(value)
    return True


@then('The saved json has body')
def saved_json(context):
    body = context.text
    context.expected_json = json.loads(body)

    adapter = context.adapter(context.table_name, context.dynamo_url)
    print(adapter)
    print(context.item_id)
    response = adapter.get_by_id(context.item_id).to_json()

    del response['entity_id']
    for key, value in response.items():
        if isinstance(response[key], dict):
            if 'entity_id' in value.keys():
                del value['entity_id']

    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    print('response json: ', response_string_json)
    print('expected json: ', expected_string_json)
    assert response_string_json == expected_string_json


@then('The saved jsons has body')
def saved_jsons(context):
    body = context.text
    context.expected_json = json.loads(body)
    for item in context.item_id:
        adapter = context.adapter(context.table_name, context.dynamo_url)
        response = adapter.get_by_id(item).to_json()
        del response['entity_id']
        for game in response['games']:
            del game['entity_id']
        # if isinstance(item, list):
        #     for x in item:
        #         del x['entity_id']
    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    print('RESPONSE: ', response_string_json)
    print('EXPECTED: ', expected_string_json)
    assert response_string_json == expected_string_json


@then('The retrived json has body')
def check_retrieved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    response_string_json = json.dumps(context.response.body['data'], sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    print('RESPONSE: ', response_string_json)
    print('EXPECTED: ', expected_string_json)
    assert response_string_json == expected_string_json


def deleted(context):
    found = False
    adapter = context.adapter(context.table_name, context.dynamo_url)

    if hasattr(context, 'list_deleted_id'):
        list_all = [x.entity_id for x in adapter.list_all()]
        for deleted_id in context.list_deleted_id:
            if deleted_id in list_all:
                found = True
    else:
        for item in adapter.list_all():
            if context.deleted_id == item.entity_id:
                found = True
    return True if not found else False


@then('I delete the test entry')
def check_delete_test_entry(context):
    adapter = context.adapter(context.table_name, context.dynamo_url)
    if hasattr(context, 'dict_list_get_all'):
        context.list_deleted_id = []
        for dict in context.dict_list_get_all:
            context.list_deleted_id.append(adapter.delete(dict['entity_id']))
        assert deleted(context)
    else:
        context.deleted_id = adapter.delete(context.item_id)
        assert deleted(context)
    assert adapter.list_all() == []


@then('I clean the {table_name} table')
def clean_table(context, table_name):
    adapter = context.adapter(table_name.lower(), context.dynamo_url)
    id_list = [x.entity_id for x in adapter.list_all()]
    for item in id_list:
        adapter.delete(item)
    assert adapter.list_all() == []


@then('I delete the test game entry')
def delete_game(context):
    adapter = context.adapter(context.table_name, context.dynamo_url)
    if hasattr(context, 'list_get_game'):
        consoles = adapter.list_all()
        for console in consoles:
            adapter.delete(console.entity_id)
    if hasattr(context, 'item_id') and isinstance(context.item_id, list):
        for x in context.item_id:
            adapter.delete(x)
    else:
        consoles = adapter.list_all()
        for console in consoles:
            games_id_list = [x.entity_id for x in console.games]
            if context.item_id in games_id_list:
                adapter.delete(console.entity_id)
            elif not games_id_list:
                adapter.delete(console.entity_id)
    assert adapter.list_all() == []


@then('The updated entry json has body')
def check_updated_json(context):
    body = context.text
    context.json_body = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)
    response = adapter.get_by_id(context.item_id).to_json()
    assert context.json_body == response


@then('The updated game entry json has body')
def check_updated_json(context):
    body = context.text
    context.json_body = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)
    response = adapter.get_by_id(context.item_id[0]).to_json()
    assert context.json_body == response
