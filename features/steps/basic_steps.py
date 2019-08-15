from behave import *
import json


@given("The request has json body")
def json_body(context):
    body = context.text
    context.json_body = json.loads(body)


@given("I create a dynamodb mock")
def dynamodb_mock(context):


