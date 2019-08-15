from app import app
from behave import *
import json
from playerstars_adapters import ConsoleAdapter


class Object(object):
    pass


convert_string_to_adapter = {
    'Console': ConsoleAdapter
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


@when('{method} request is made to {url}')
def json_request(context, method, url):
    if 'json_body' in context:
        app.current_request = Object()
        app.current_request.json_body = context.json_body

    url_method = app.routes.get(url)[method.upper()]
    response = url_method.view_function()

    # response = app.routes.get(url)[method.upper()].view_function().body
    context.response = response
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
    print(context.response.body)
    context.item_id = context.response.body
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


@then('The retrived json has body')
def check_retrieved_json(context):
    body = context.text
    context.expected_json = json.loads(body)
    response_string_json = json.dumps(context.response.body['data'], sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


@then('I delete the test entry')
def delete_test_entry(context):
    context.deleted_id = context.adapter().delete(context.item_id)
    assert deleted(context)
