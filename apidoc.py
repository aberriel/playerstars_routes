import json
from typing import List, Dict, Any, Callable

from pydantic import BaseModel
from pydantic.schema import model_schema

from app import app


class ContentExample:
    def __init__(self,
                 summary: str,
                 description: str,
                 value: Any,
                 name: str):
        self.summary = summary
        self.description = description
        self.value = value
        self.name = name

    def render(self):
        return {
            self.name: {
                'summary': self.summary,
                'description': self.description,
                'value': self.value
            }
        }


class ResponseContent:
    def __init__(self,
                 media_type: str,
                 schema: dict,
                 examples: [List[ContentExample], None] = None):
        self.media_type = media_type
        self.schema = schema
        self.examples = examples

    def render(self):
        mt = self.media_type
        rendered = {
            mt: {
                'schema': self.schema
            }
        }
        if self.examples is not None:
            if len(self.examples) == 1:
                rendered[mt]['example'] = {}
                rendered[mt]['example'].update(self.examples[0].render())
            else:
                rendered[mt]['examples'] = {
                    x.name: x.render() for x in self.examples
                }

        return rendered


class MethodResponse:
    def __init__(self,
                 status_code: int,
                 description: str,
                 content: [ResponseContent, None] = None):
        self.status_code = status_code
        self.description: str = description
        self.content = content

    def render(self):
        response_key = str(self.status_code)
        rendered = {
            response_key: {
                'description': self.description
            }
        }
        if self.content is not None:
            rendered[response_key]['content'] = self.content.render()

        return rendered


class MethodParameter:
    def __init__(self,
                 name: str,
                 location: str,
                 required: bool,
                 description: str,
                 schema: [Dict, None] = None):
        self.name = name
        self.location = location
        self.required = required
        self.description = description
        self.schema = schema if schema is not None else {}

    def render(self):
        return {
            'name': self.name,
            'in': self.location,
            'required': self.required,
            'description': self.description,
            'schema': self.schema
        }


class DefaultResponse200(BaseModel):
    status: str = 'success'
    data: Any


class DefaultResponse500(BaseModel):
    status: str = 'error'
    data: str


def get_openapi_schema(model):
    _schema = model_schema(model, ref_prefix='#/components/schemas/')
    defs = None
    if 'definitions' in _schema:
        defs = _schema.pop('definitions')
    return _schema, defs


class PathMethod:
    def __init__(self,
                 method: str,
                 tags: List[str],
                 summary: str,
                 operation_id: str,
                 register_schema_fn: Callable):
        self.method: str = method.lower()
        self.tags: List[str] = tags
        self.summary: str = summary
        self.operation_id: str = operation_id
        self.responses: List[MethodResponse] = []
        self.parameters: List[MethodParameter] = []
        self.register_schema = register_schema_fn

    def append_response(self, response: MethodResponse):
        self.responses.append(response)

    def append_parameter(self, parameter: MethodParameter):
        self.parameters.append(parameter)

    def _get_schema(self, model):
        _schema, defs = get_openapi_schema(model)
        if defs is not None:
            self.register_schema(defs)
        return _schema

    def _get_content(self,
                     model,
                     media_type='application/json',
                     example=None):
        _schema = self._get_schema(model)
        args = [media_type, _schema]
        if example is not None:
            args.append([example])
        return ResponseContent(*args)

    def _get_default_responses(self):
        responses = {}
        example_200 = {'status': 'success', 'data': {'entity_id': '2f5a192f'}}
        example200 = ContentExample('Successful',
                                    'A Successful response',
                                    example_200,
                                    name='Success')

        default_200 = MethodResponse(200,
                                     'Default success response',
                                     self._get_content(DefaultResponse200,
                                                       example=example200))

        example_500 = {'status': 'error', 'message': 'Internal Server Error'}
        example500 = ContentExample('Error',
                                    'Error not handled',
                                    example_500,
                                    name='Error')
        default_500 = MethodResponse(500,
                                     'Default error response',
                                     self._get_content(DefaultResponse500,
                                                       example=example500))

        responses.update(default_200.render())
        responses.update(default_500.render())

        return responses

    def render(self):
        responses = {}
        for response in self.responses:
            responses.update(response.render())

        if not responses:
            responses = self._get_default_responses()

        parameters = [x.render() for x in self.parameters]

        rendered = {
            self.method: {
                'tags': self.tags,
                'summary': self.summary,
                'operationId': self.operation_id
            }
        }
        rendered[self.method].update({'responses': responses})

        if parameters:
            rendered[self.method].update({'parameters': parameters})

        return rendered


class ApiPath:
    def __init__(self,
                 path: str):
        self.path: str = path
        self.methods: List[PathMethod] = []

    def append_method(self, method: PathMethod):
        self.methods.append(method)

    def render(self):
        rendered = {}
        for method in self.methods:
            rendered.update(method.render())

        return {self.path: rendered}


class OpenApiSpec:
    def __init__(self,
                 title: str,
                 description: str,
                 version: str):
        self.title = title
        self.description = description
        self.version = version
        self.paths: List[ApiPath] = []
        self.components = []

    def append_path(self, path: ApiPath):
        self.paths.append(path)

    def register_schema(self, the_schema):
        self.components.append(the_schema)

    def render(self):
        rendered = {
            'openapi': "3.0.2",
            'info': {
                'title': self.title,
                'description': self.description,
                'version': self.version
            }
        }
        paths = {}
        for path in self.paths:
            paths.update(path.render())

        if paths:
            rendered.update({'paths': paths})

        if self.components:
            rendered.update({'components': {'schemas': {}}})
        for component in self.components:
            rendered['components']['schemas'].update(component)

        return rendered


def get_parameters(path):
    parameters = []

    for part in [x for x in path.split('/') if x]:
        if part[0] == '{' and part[-1] == '}':
            parameters.append(
                MethodParameter(part[1:-1],
                                'path',
                                True,
                                ''))
    return parameters


def run():
    api = OpenApiSpec(title='PlayerStars Backend',
                      description='API do Sistema PlayerStars',
                      version="0.1.0")

    for routepath, route in app.routes.items():
        path = ApiPath(routepath)

        for method_name, route_entry in route.items():
            method = PathMethod(method=method_name.lower(),
                                tags=[],
                                summary='',
                                operation_id='',
                                register_schema_fn=api.register_schema)

            annotation = route_entry.view_function.__annotations__
            if 'return' in annotation:
                for response in filter(lambda x: issubclass(x, BaseModel),
                                       annotation['return']):
                    _schema, defs = get_openapi_schema(response)
                    if defs is not None:
                        api.register_schema(defs)

                    content = ResponseContent('application/json', _schema)
                    method_response = MethodResponse(
                        status_code=response.status_code(),
                        description=response.__doc__,
                        content=content)
                    method.append_response(method_response)

            for parameter in get_parameters(routepath):
                method.append_parameter(parameter)

            path.append_method(method)

        api.append_path(path)

    with open('doc/openapi.json', 'w+') as f:
        f.write(json.dumps(api.render()))


if __name__ == '__main__':
    run()
