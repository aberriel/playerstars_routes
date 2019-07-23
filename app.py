from chalice import Chalice

from playerstars_routes import root
# from chalicelib.settings import Settings

app = Chalice(app_name='playerstars')
# app.log.setLevel(Settings.LOG_LEVEL)

app.experimental_feature_flags.update([
    'BLUEPRINTS'
])

app.register_blueprint(root, url_prefix='/')
# app.register_blueprint(bp_express_checkout, url_prefix='/gateway')
# app.register_blueprint(bp_pagseguro, url_prefix='/pagseguro')
# app.register_blueprint(bp_produto, url_prefix='/')


@app.route('/check')
def index():
    return {'status': 'ok',
            'data': 'Aune Live is ALIVE!!!!'}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
# from chalice import Chalice
#
# app = Chalice(app_name='chalice_routes')
#
#
# @app.route('/')
# def index():
#     return {'hello': 'world'}

