import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from chalicelib.dashboard.dashboard_utils import DashboardUtils

prefix = 'chalicelib.dashboard.dashboard_utils'


class TestDashboardUtils(TestCase):
    def setUp(self):
        self.settings_patch = patch(f'{prefix}.Settings',
                                    ENVIRONMENT='dev')
        self.adapter_patch = patch(f'{prefix}.DashboardAdapter')
        self.interactor_patch = patch(f'{prefix}.DashboardInteractor')
        self.mock_app = MagicMock()

        def factory():
            return DashboardUtils(self.mock_app)

        self.factory = factory

        self.mock_settings = self.settings_patch.start()
        self.mock_adapter = self.adapter_patch.start()
        self.mock_interactor = self.interactor_patch.start()

    def tearDown(self):
        self.settings_patch.stop()
        self.adapter_patch.stop()
        self.interactor_patch.stop()

    def test_send_preduel_creation(self):
        du = self.factory()
        mock_preduel_id = 'mocked_id'
        du.send_preduel_creation(mock_preduel_id)

        expected = json.dumps({
            "event": "preduel_creation",
            "preduel_id": mock_preduel_id
        })

        self.mock_interactor().broadcast.assert_called_with(expected)

    def test_send_preduel_match(self):
        du = self.factory()
        mock_preduel_id = 'mocked_id'
        du.send_preduel_match(mock_preduel_id)

        expected = json.dumps({
            "event": "preduel_match",
            "preduel_id": mock_preduel_id
        })

        self.mock_interactor().broadcast.assert_called_with(expected)
