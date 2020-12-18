import os
from datetime import datetime

from aws_task_scheduler import AwsTaskSchedulerAdapter
from boto3 import Session
from chalice import Chalice
from playerstars_adapters import EventReminderAssistantAdapter
from playerstars_domain import EraAction

from chalicelib import root
from chalicelib.admin.preduel_routes import get_preduel_admin_routes
from chalicelib.admin_routes import bp_admin
from chalicelib.console_route import (
    bp_console,
    bp_console_admin,
    bp_console_external)
from chalicelib.convert_star_rate_route import bp_convert
from chalicelib.dashboard.dashboard_adapter import DashboardAdapter, \
    NullDashboardAdapter
from chalicelib.dashboard.dashboard_entity import DashboardEntity
from chalicelib.dashboard.dashboard_interactors import DashboardInteractor, \
    NullDashboardInteractor
from chalicelib.dashboard.dashboard_utils import DashboardUtils
from chalicelib.duel_route import (
    bp_cancel_duel,
    bp_create_duel,
    bp_duel,
    bp_enter_duel,
    bp_inform_invite_timeout,
    bp_match_list)
from chalicelib.duel_scheduled_finisher import duel_scheduled_finisher
from chalicelib.era_routes import EraRunner
from chalicelib.era_routes import bp_era_finish_duel
from chalicelib.era_routes import era_factory
from chalicelib.game_route import bp_game, bp_game_by_console
from chalicelib.mail_routes import (
    bp_contact_email, bp_invitation_email, bp_welcome_email)
from chalicelib.notification_route import (
    bp_notification,
    bp_notification_read)
from chalicelib.pagseguro_purchase_route import bp_purchase
from chalicelib.player_route import bp_player, bp_player_by_console
from chalicelib.product_route import bp_plan, bp_product
from chalicelib.purchase import (
    bp_google,
    bp_webhook_wirecard,
    bp_wirecard)
from chalicelib.region_country_route import bp_region_country
from chalicelib.region_state_route import bp_region_state
from chalicelib.settings import Settings
from chalicelib.team_route import bp_enter_team, bp_team
from chalicelib.terms_policy_route import bp_terms, bp_policy
from chalicelib.tournament.get_tournament_detail import tournament_route
from chalicelib.user_admin_route import bp_user_admin
from chalicelib.values_route import bp_value

app = Chalice(app_name='PlayerStars')
app.experimental_feature_flags.update(['BLUEPRINTS', 'WEBSOCKETS'])
app.websocket_api.session = Session()
app.websocket_api.configure(os.environ.get('WS_DOMAIN'), 'dev')

app.register_blueprint(root)

app.register_blueprint(bp_admin, url_prefix='/admin')
app.register_blueprint(get_preduel_admin_routes(), url_prefix='/admin')

app.register_blueprint(bp_cancel_duel, url_prefix='/cancel-duel')
app.register_blueprint(bp_console, url_prefix='/console')
app.register_blueprint(bp_console_admin, url_prefix='/admin/console')
app.register_blueprint(bp_console_external, url_prefix='/console/external')
app.register_blueprint(bp_convert, url_prefix='/convert-rate')
app.register_blueprint(bp_create_duel, url_prefix='/create-duel')
app.register_blueprint(bp_duel, url_prefix='/duel')
app.register_blueprint(bp_enter_duel, url_prefix='/enter-duel')
app.register_blueprint(bp_enter_team, url_prefix='/enter')
app.register_blueprint(bp_game, url_prefix='/game')
app.register_blueprint(bp_game_by_console, url_prefix='/game/console')
app.register_blueprint(bp_google, url_prefix='/purchase/google')
app.register_blueprint(bp_contact_email, url_prefix='/contact-email')
app.register_blueprint(bp_inform_invite_timeout,
                       url_prefix='/duel/inform-invite-timeout')
app.register_blueprint(bp_invitation_email, url_prefix='/invitation-email')
app.register_blueprint(bp_welcome_email, url_prefix='/welcome-email')
app.register_blueprint(bp_match_list, url_prefix='/match-list')
app.register_blueprint(bp_notification, url_prefix='/notification')
app.register_blueprint(bp_notification_read,
                       url_prefix='/notification/set-as-read')
app.register_blueprint(bp_player, url_prefix='/player')
app.register_blueprint(bp_player_by_console, url_prefix='/player-by-game')
app.register_blueprint(bp_plan, url_prefix='/plan')
app.register_blueprint(bp_product, url_prefix='/product')
app.register_blueprint(bp_policy, url_prefix='/privacy-policy')
app.register_blueprint(bp_purchase, url_prefix='/purchase')
app.register_blueprint(bp_region_country, url_prefix='/region-country')
app.register_blueprint(bp_region_state, url_prefix='/region-state')
app.register_blueprint(bp_team, url_prefix='/team')
app.register_blueprint(bp_terms, url_prefix='/terms-and-conditions')
app.register_blueprint(bp_user_admin, url_prefix='/user-admin')
app.register_blueprint(bp_value, url_prefix='/values')
app.register_blueprint(bp_webhook_wirecard,
                       url_prefix='/purchase/wirecard/webhook')
app.register_blueprint(bp_wirecard, url_prefix='/purchase/wirecard')
app.register_blueprint(tournament_route, url_prefix='/tournament')

app.register_blueprint(bp_era_finish_duel, url_prefix='/era-finish-duel')


@app.route('/check', methods=['POST', 'GET'])
def index():
    return {
        'status': 'ok',
        'data': 'PlayerStars is alive!!'}


@app.route('/test_era', methods=['POST'])
def do_era_test():
    try:
        body = app.current_request.json_body

        cmd = body['command']
        if cmd == 'SET_ERA':
            """
                Command SET_ERA:
                {
                    "command": "SET_ERA",
                    "event": {
                        "action": {
                            "url": "https://url_para_chamar.com/resource",
                            "method": "GET|POST|PUT|DELETE",
                            "payload": {
                                "answer": 42
                            }
                        },
                        "name": "Me acorde",
                        "event_time": "datetime_utc_iso"
                    },
                    "scheduler": {
                        "name": "test_scheduler"
                    }
                }
            """
            persist_adapter = EventReminderAssistantAdapter(
                table_name=Settings.ERA_TABLE_NAME)
            scheduler_adapter = AwsTaskSchedulerAdapter(
                name=body['scheduler']['name'],
                lambda_runner=get_era_runner_name()
            )
            action = body['event']['action']
            era_action = EraAction(
                url=action['url'],
                method=action['method'],
                payload=action['payload']
            )
            event = body['event']
            era = era_factory(
                name=event['name'],
                event_time=datetime.fromisoformat(event['event_time']),
                action=era_action,
                persist_adapter=persist_adapter,
                scheduler_adapter=scheduler_adapter
            )
            era.save()

            return {
                'Sucesso': {
                    'Era Id': era.entity_id
                }
            }
    except Exception as e:
        return {
            'Erro': {
                'Class': e.__class__.__name__,
                'Value': str(e)
            }
        }


@app.lambda_function(name=Settings.DUEL_SCHEDULED_FINISHER_NAME)
def duel_finish_handler(event, context):
    return duel_scheduled_finisher(event['duel_id'])


def get_era_runner_name():
    app_name = Settings.ERA_AWS_LAMBDA_FUNCTION_NAME
    runner_name = Settings.ERA_RUNNER_NAME

    return f'{app_name}-{runner_name}'


@app.lambda_function(name=Settings.ERA_RUNNER_NAME)
def era_runner(event, context):
    scheduler_name = event['scheduler_name']
    era_id = event['era_id']

    scheduler_adapter = AwsTaskSchedulerAdapter(
        name=scheduler_name,
        lambda_runner=get_era_runner_name())

    persist_adapter = EventReminderAssistantAdapter(
        table_name=Settings.ERA_TABLE_NAME)

    runner = EraRunner(era_id=era_id,
                       scheduler_adapter=scheduler_adapter,
                       persist_adapter=persist_adapter)

    runner.run()


# Websocket Handlers

# table_name definido aqui mesmo, pois
# não deve existir em nenhum outro ambiente
if Settings.ENVIRONMENT == 'dev':
    dashboard_adapter = DashboardAdapter('dashboard_dev')
    dashboard_interactor = DashboardInteractor(app, dashboard_adapter)
else:
    dashboard_adapter = NullDashboardAdapter('dummy')
    dashboard_interactor = NullDashboardInteractor(app, dashboard_adapter)


dashboard_utils = DashboardUtils(app)


@app.on_ws_connect()
def connect(event):
    dashboard = DashboardEntity(event.connection_id)
    dashboard.set_adapter(dashboard_adapter)
    dashboard.save()


@app.on_ws_disconnect()
def disconnect(event):
    dashboard_adapter.delete(event.connection_id)


@app.on_ws_message()
def ws_message(event):
    dashboard_interactor.handle_message(event.connection_id, event.body)
