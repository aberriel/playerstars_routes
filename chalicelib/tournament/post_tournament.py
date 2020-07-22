from chalice_support import bad_request, success, server_error
from marshmallow import ValidationError
from playerstars_adapters import PlayerTournamentAdapter, \
    TeamTournamentAdapter, ConsoleAdapter, ValuesAdapter
from playerstars_domain import DuelType
from playerstars_interactors.tournament.post_tournament_interactor import \
    PostTournamentRestModel, PostTournamentInteractor, PostTournamentAdapters
from playerstars_interactors.utils.report_exception import exception_str

from chalicelib.private_route import PrivateRoute
from chalice_support.jwt import JwtUtils

from chalicelib.settings import Settings

tournament_route = PrivateRoute(__name__)


def _get_tournament_adapter(request: PostTournamentRestModel):
    adapter_map = {
        DuelType.INDIVIDUAL: (PlayerTournamentAdapter,
                              Settings.PLAYER_TOURNAMENT_TABLE_NAME),
        DuelType.CHAMPIONSHIP: (TeamTournamentAdapter,
                                Settings.TEAM_TOURNAMENT_TABLE_NAME)
    }

    klass, table_name = adapter_map[request.duel_type]

    return klass(table_name=table_name)


def _get_console_adapter():
    return ConsoleAdapter(table_name=Settings.CONSOLE_TABLE_NAME)


def _get_values_adapter():
    return ValuesAdapter(table_name=Settings.VALUES_TABLE_NAME)


@tournament_route.post('/')
def post_tournament():
    ju = JwtUtils(tournament_route)
    player_id = ju.get_username_from_jwt()
    json_body = tournament_route.current_request.json_body

    try:
        request = PostTournamentRestModel.from_json(json_body)
    except ValidationError as e:
        msg = f'Validation Error loading request: {e}'
        return bad_request(msg)

    tournament_adapter = _get_tournament_adapter(request)
    console_adapter = _get_console_adapter()
    values_adapter = _get_values_adapter()
    adapters = PostTournamentAdapters(
        tournament=tournament_adapter,
        console=console_adapter,
        values=values_adapter)

    interactor = PostTournamentInteractor(
        request=request,
        adapters=adapters,
        player_id=player_id)

    try:
        result = interactor.run()
        json_response = result.to_json()
        return success(json_response)

    except Exception as e:
        msg = f'Unknown error posting tournament: {exception_str(e)}'
        return server_error(msg)
