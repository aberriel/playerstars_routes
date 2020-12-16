from clapy_dynamodb_adapter import BasicDynamodbAdapter

from chalicelib.dashboard.dashboard_entity import DashboardEntity


class DashboardAdapter(BasicDynamodbAdapter):
    def __init__(self, table_name: str):
        super().__init__(table_name=table_name,
                         db_endpoint=None,
                         adapted_class=DashboardEntity)


# noinspection PyMethodMayBeStatic
class NullDashboardAdapter:
    def __init__(self, table_name: str):
        pass

    def list_all(self):
        return []

    def get_by_id(self, item_id):
        return None

    def save(self, json_data):
        return ''

    def delete(self, entity_id):
        return entity_id

    def filter(self, **kwargs):
        return []
