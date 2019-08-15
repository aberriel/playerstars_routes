from app import app
from behave import *
import json
import httpretty


class Object(object):
    pass


@given("The request has json body")
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@when('{method} request is made to {url}')
def json_request(context, method, url):
    if 'json_body' in context:
        app.current_request = Object()
        app.current_request.json_body = context.json_body

    url_method = app.routes.get(url)[method.upper()]
    function = url_method.view_function()
    response = function.body

    # response = app.routes.get(url)[method.upper()].view_function().body
    context.response = response
    print(context.response)
    try:
        context.response.json = json.loads(context.response)
    except Exception:
        pass
