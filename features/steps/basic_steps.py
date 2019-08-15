from app import app
from behave import *
import json
import boto3
from playerstars_adapters import ConsoleAdapter


class Object(object):
    pass


@given('The request has json body')
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@given('I set table name as {table_name}')
def json_body(context, table_name):
    context.table_name = table_name


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


@then('The response should have status {status}')
def json_response_status(context, status):
    assert context.response.body['status'] == status


@then('The response should have status_code {status_code}')
def json_response_status_code(context, status_code):
    assert context.response.status_code == int(status_code)


convert_string_to_adapter = {
    'Console': ConsoleAdapter
}


@then('The saved json has body')
def saved_json(context):
    body = context.text
    context.expected_json = json.loads(body)

    response = convert_string_to_adapter[context.table_name]().get_by_id(context.item_id).to_json()
    del response['entity_id']

    response_string_json = json.dumps(response, sort_keys=True)
    expected_string_json = json.dumps(context.expected_json, sort_keys=True)
    assert response_string_json == expected_string_json


@then('I delete the test entry')
def delete_test_entry(context):
    found = False
    response = convert_string_to_adapter[context.table_name]().delete(context.item_id)
    for item in convert_string_to_adapter[context.table_name]().list_all():
        if response == item.entity_id:
            found = True
    assert not found
