from typing import List

from chalice import Chalice, WebsocketDisconnectedError

from chalicelib.dashboard.dashboard_adapter import DashboardAdapter, NullDashboardAdapter
from chalicelib.dashboard.dashboard_entity import DashboardEntity


class DashboardInteractor:
    def __init__(self, app: Chalice, dashboard_adapter: DashboardAdapter):
        self.app = app
        self.adapter = dashboard_adapter

    def send(self, connection_id, message):
        try:
            self.app.websocket_api.send(connection_id, message)
        except WebsocketDisconnectedError as e:
            # If the websocket has been closed, we delete the connection from our database.
            self.adapter.delete(e.connection_id)

    def broadcast(self, message):
        all_connections: List[DashboardEntity] = self.adapter.list_all()
        for dashboard in all_connections:
            self.send(dashboard.entity_id, message)

    def register_connection(self, connection_id):
        dashboard = DashboardEntity(connection_id)
        dashboard.set_adapter(self.adapter)
        dashboard.save()

    def remove_connection(self, connection_id):
        self.adapter.delete(connection_id)

    def handle_message(self, connection_id, body):
        pass


class NullDashboardInteractor:
    def __init__(self, app, dashboard_adapter: NullDashboardAdapter):
        pass

    def send(self, connection_id, message):
        pass

    def broadcast(self, message):
        pass

    def register_connection(self, connection_id):
        pass

    def remove_connection(self, connection_id):
        pass

    def handle_message(self, connection_id, body):
        pass
