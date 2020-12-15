from clapy_basic_classes import BasicEntity
from marshmallow import post_load


class DashboardEntity(BasicEntity):
    def __init__(self,
                 entity_id=None):
        super().__init__(entity_id)

    class Schema(BasicEntity.Schema):
        @post_load
        def on_load(self, data, many, partial):
            return DashboardEntity(**data)
