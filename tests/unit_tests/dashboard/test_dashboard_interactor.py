from collections import namedtuple
from unittest.mock import MagicMock, patch, call

from chalice import WebsocketDisconnectedError
from pytest import fixture

from chalicelib.dashboard.dashboard_entity import DashboardEntity
from chalicelib.dashboard.dashboard_interactors import DashboardInteractor, \
    NullDashboardInteractor

TInteractor = namedtuple('TInteractor', 'interactor, mock_app, mock_adapter')
prefix = 'chalicelib.dashboard.dashboard_interactors'


@fixture
def interactor():
    def interactor_factory(mock_app=MagicMock(),
                           mock_adapter=MagicMock()):
        interactor = DashboardInteractor(mock_app, mock_adapter)
        return TInteractor(interactor, mock_app, mock_adapter)

    return interactor_factory


def test_dashboard_interactor(interactor):
    mock_app = MagicMock()
    mock_adapter = MagicMock()
    interactor = interactor(mock_app, mock_adapter).interactor

    assert interactor.app == mock_app
    assert interactor.adapter == mock_adapter


def test_dashboard_interactor_sned(interactor):
    interactor, mock_app, mock_adapter = interactor()

    mock_cid = MagicMock()
    mock_msg = MagicMock()
    interactor.send(mock_cid, mock_msg)

    mock_app.websocket_api.send.assert_called_with(mock_cid, mock_msg)


def test_dashboard_interactor_send_disconected(interactor):
    mock_app = MagicMock(
        websocket_api=MagicMock(
            send=MagicMock(
                side_effect=WebsocketDisconnectedError(connection_id='cid'))))
    interactor, mock_app, mock_adapter = interactor(mock_app=mock_app)

    mock_cid = MagicMock()
    mock_msg = MagicMock()
    interactor.send(mock_cid, mock_msg)
    mock_adapter.delete.assert_called_with('cid')


@patch.object(DashboardInteractor, 'send')
def test_dashboard_interactor_broadcast(mock_send, interactor):
    mock_adapter = MagicMock(list_all=MagicMock(return_value=[
        DashboardEntity('cid1'), DashboardEntity('cid2')]))
    interactor, mock_app, mock_adapter = interactor(mock_adapter=mock_adapter)

    mock_msg = MagicMock()
    interactor.broadcast(mock_msg)

    mock_send.assert_has_calls([call('cid1', mock_msg),
                                call('cid2', mock_msg)])


@patch(f'{prefix}.DashboardEntity')
def test_dashboard_interactor_register_connection(mock_entity,
                                                  interactor):
    interactor, mock_app, mock_adapter = interactor()

    mock_connection_id = MagicMock()
    interactor.register_connection(mock_connection_id)

    mock_entity.assert_called_with(mock_connection_id)
    mock_entity().set_adapter.assert_called_with(mock_adapter)
    mock_entity().save.assert_called_once()


def test_dashboard_interactor_remove_connection(interactor):
    interactor, mock_app, mock_adapter = interactor()

    mock_cid = MagicMock()
    interactor.remove_connection(mock_cid)

    mock_adapter.delete.assert_called_with(mock_cid)


def test_null_dashboard_interactor():
    mock_app = MagicMock()
    mock_adapter = MagicMock()
    ndi = NullDashboardInteractor(mock_app, mock_adapter)

    mock_cid = MagicMock()
    mock_msg = MagicMock()
    mock_body = MagicMock()
    assert ndi.send(mock_cid, mock_msg) is None
    assert ndi.broadcast(mock_msg) is None
    assert ndi.register_connection(mock_cid) is None
    assert ndi.remove_connection(mock_cid) is None
    assert ndi.handle_message(mock_cid, mock_body) is None
