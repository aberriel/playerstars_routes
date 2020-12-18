from chalicelib.dashboard.dashboard_adapter import NullDashboardAdapter, \
    DashboardAdapter
from chalicelib.dashboard.dashboard_interactors import DashboardInteractor, \
    NullDashboardInteractor
from chalicelib.settings import Settings


class DashboardUtils:
    def __init__(self):
        from app import app
        if Settings.ENVIRONMENT == 'dev':
            adapter = DashboardAdapter(table_name='dashboard_dev')
            self.interactor = DashboardInteractor(app, adapter)
        else:
            adapter = NullDashboardAdapter('dummy')
            self.interactor = NullDashboardInteractor(app, adapter)

    def send_preduel_creation(self, preduel_id):
        message = {
            "event": "preduel_creation",
            "preduel_id": preduel_id
        }
        self.interactor.broadcast(message)

    def send_preduel_match(self, preduel_id):
        message = {
            "event": "preduel_match",
            "preduel_id": preduel_id
        }
        self.interactor.broadcast(message)
