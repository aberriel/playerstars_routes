from app import app
from behave import *
import json
from chalicelib.settings import Settings
from playerstars_adapters import (ConsoleAdapter, CountryRegionAdapter,
                                  StateRegionAdapter, UserAdminAdapter,
                                  PlayerAdapter)


class Object(object):
    pass


convert_string_to_adapter = {
    'console': ConsoleAdapter,
    'regioncountry': CountryRegionAdapter,
    'regionstate': StateRegionAdapter,
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
        app.current_request.json_body = context.json_body

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
        app.current_request.json_body = context.json_body
    url_method = app.routes.get(url+"/{entity_id}")[method.upper()]
    response = url_method.view_function(entity_id)
    context.response = response
    if method.upper() in ['GET']:
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
    assert context.response.status_code == int(status_code)


@given('The request has json body')
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@then('The saved json has body')
def saved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    print("context-Json-----", context.item_id)
    print("context-Json-----", context.table_name)

    adapter = context.adapter(context.table_name, context.dynamo_url)
    response = adapter.get_by_id(context.item_id).to_json()

    del response['entity_id']
    for key, value in response.items():
        if isinstance(response[key], dict):
            del value['entity_id']

    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
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
    # print('RESPONSE: ', response_string_json)
    # print('EXPECTED: ', expected_string_json)
    assert response_string_json == expected_string_json


@then('The retrived json has body')
def check_retrieved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    response_string_json = json.dumps(context.response.body['data'], sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


def deleted(context):
    found = False
    adapter = context.adapter(context.table_name, context.dynamo_url)

    if hasattr(context, 'list_deleted_id'):
        print("SE EU ENTREI AQUI< TEM ALGUMA COISA MUITO ERRADA")
        list_all = [x.entity_id for x in adapter.list_all()]
        for deleted_id in context.list_deleted_id:
            if deleted_id in list_all:
                found = True
    else:
        for item in adapter.list_all():
            print("$$$$$$$$: ", item)
            if context.deleted_id == item.entity_id:
                found = True
    return True if not found else False


@then('I delete the test entry')
def check_delete_test_entry(context):
    adapter = context.adapter(context.table_name, context.dynamo_url)
    if hasattr(context, 'dict_list_get_all'):
        context.list_deleted_id = []
        print("DICT LIST GET ALL: ", context.dict_list_get_all)
        for dict in context.dict_list_get_all:
            print("DICT PARA DELETAR: ", dict)
            context.list_deleted_id.append(adapter.delete(dict['entity_id']))
        print("DELETADOS: ", context.list_deleted_id)
        assert deleted(context)
    else:
        print(context.item_id)
        context.deleted_id = adapter.delete(context.item_id)
        assert deleted(context)
    assert adapter.list_all() == []


@then('The updated entry json has body')
def check_updated_json(context):
    body = context.text
    context.json_body = json.loads(body)
    adapter = context.adapter(context.table_name, context.dynamo_url)

    response = adapter.get_by_id(context.item_id).to_json()
    assert context.json_body == response
