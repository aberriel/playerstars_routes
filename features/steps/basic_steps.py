from app import app
from behave import *
import json
from playerstars_adapters import ConsoleAdapter, CountryRegionAdapter


class Object(object):
    pass


convert_string_to_adapter = {
    'Console': ConsoleAdapter,
    'RegionCountry': CountryRegionAdapter
}


def saved(context):
    found = False
    for item in context.adapter().list_all():
        if context.saved_entity_id == item.entity_id:
            found = True
    return True if found else False


def deleted(context):
    found = False
    for item in context.adapter().list_all():
        if context.deleted_id == item.entity_id:
            found = True
    return True if not found else False


@given('I set table name and the adapter class as {table_name}')
def json_body(context, table_name):
    context.table_name = table_name
    context.adapter = convert_string_to_adapter[context.table_name]


@given('The request has json body')
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@given('I save a new entry to the database with json body')
def save_new_entry(context):
    body = context.text
    context.json_body = json.loads(body)

    context.saved_entity_id = context.adapter().save(context.json_body)
    assert saved(context)


@given('I emptied the database')
def data_base_is_empty(context):
    get_all_consoles = context.adapter().list_all
    if get_all_consoles():
        for item in get_all_consoles():
            context.adapter().delete(item.entity_id)
    database_after_delete = get_all_consoles()
    assert database_after_delete == []


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


@then('The saved json has body')
def saved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    response = context.adapter().get_by_id(context.item_id).to_json()
    del response['entity_id']
    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


@then('The saved jsons has body')
def saved_jsons(context):
    body = context.text
    context.expected_json = json.loads(body)
    for item in context.item_id:
        response = context.adapter().get_by_id(item).to_json()
        del response['entity_id']
        for game in response['games']:
            del game['entity_id']
    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


@then('The retrived json has body')
def check_retrieved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    response_string_json = json.dumps(context.response.body['data'], sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


@then('I delete the test entry')
def check_delete_test_entry(context):
    if hasattr(context, 'dict_list_get_all'):
        for key in context.dict_list_get_all.keys():
            context.deleted_id = context.adapter().delete(key)
    context.deleted_id = context.adapter().delete(context.item_id)
    assert deleted(context)


@then('The updated entry json has body')
def check_updated_json(context):
    body = context.text
    context.json_body = json.loads(body)
    response = context.adapter().get_by_id(context.item_id).to_json()
    assert context.json_body == response
