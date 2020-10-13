from collections import namedtuple
from datetime import datetime
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch
import pytest
from clapy_basic_classes.basic_domain.util import \
    generic_serialize_roundtrip_test
from playerstars_domain.utils.datetime_helper import aware_utc
from pytest import raises, fixture
from chalicelib.era_routes import BasicTaskSchedulerAdapter, \
    TaskSchedulerPort, EventReminderAssistant, _extend_dict, EraRunner
from playerstars_domain import EraAction
from playerstars_domain.event_reminder_assistant.\
    event_reminder_assistant import era_factory


def test_basic_task_scheduler_adapter():
    mock_set = MagicMock()
    mock_update = MagicMock()
    mock_delete = MagicMock()

    class TestClass(BasicTaskSchedulerAdapter):
        def set(self, task_identifier: str, execution_time: datetime):
            super().set(task_identifier, execution_time)
            mock_set(task_identifier, execution_time)

        def update(self, task_identifier: str, execution_time: datetime):
            super().update(task_identifier, execution_time)
            mock_update(task_identifier, execution_time)

        def delete(self):
            super().delete()
            mock_delete()

        @classmethod
        def get_current(cls, name: str):
            pass

        def __init__(self,
                     name: str,
                     task_id: Optional[str] = None,
                     execution_time: Optional[datetime] = None):
            super().__init__(name, task_id, execution_time)

    mock_name = MagicMock()
    mock_task_id = MagicMock()
    mock_exec_time = MagicMock()

    test_obj = TestClass(mock_name)
    test_obj.set(mock_task_id, mock_exec_time)
    mock_set.assert_called_with(mock_task_id, mock_exec_time)
    assert test_obj.execution_time == mock_exec_time
    assert test_obj.task_id == mock_task_id

    test_obj2 = TestClass(mock_name)
    test_obj2.set(mock_task_id, mock_exec_time)

    mock_new_id = MagicMock()
    mock_new_exec_time = MagicMock()
    test_obj2.update(mock_new_id, mock_new_exec_time)
    mock_update.assert_called_with(mock_new_id, mock_new_exec_time)
    assert test_obj2.execution_time == mock_new_exec_time
    assert test_obj2.task_id == mock_new_id

    test_obj2.delete()
    mock_delete.assert_called_once()
    assert test_obj2.execution_time is None
    assert test_obj2.task_id is None

    test_obj.get_current('nada')


def test_get_current_not_implemented():
    class Test(BasicTaskSchedulerAdapter):
        def set(self, task_identifier: str, execution_time: datetime):
            pass

        def update(self, task_identifier: str, execution_time: datetime):
            pass

        def delete(self):
            pass

        @classmethod
        def get_current(cls, name: str):
            super().get_current(name)

    test = Test(MagicMock(), MagicMock(), MagicMock())
    test.set(MagicMock(), MagicMock())
    test.update(MagicMock(), MagicMock())
    test.delete()
    with raises(NotImplementedError):
        test.get_current('nome')


def test_task_scheduler_prot():
    class TestClass(TaskSchedulerPort):
        def __init__(self):
            super().__init__()

    mock_adapter = MagicMock()
    test_obj = TestClass()
    test_obj.set_scheduler_adapter(mock_adapter)

    assert test_obj.scheduler_adapter == mock_adapter

# ##########################################################################


@fixture
def url():
    return 'https://minhaapi.com/minha_acao'


Factory = namedtuple(
    'Factory',
    'era, mock_name, mock_event_time, mock_action, '
    'mock_persist_adapter, mock_scheduler_adapter')


@fixture
def era_factory_fixture():
    def factory(mock_name=MagicMock(),
                mock_event_time=MagicMock(),
                mock_action=MagicMock(),
                mock_persist_adapter=MagicMock(),
                mock_scheduler_adapter=MagicMock()) -> Factory:
        era = era_factory(mock_name,
                          mock_event_time,
                          mock_action,
                          mock_persist_adapter,
                          mock_scheduler_adapter)
        return Factory(era, mock_name, mock_event_time, mock_action,
                       mock_persist_adapter, mock_scheduler_adapter)

    return factory


def test_era_serialization(url):
    mock_name = 'dummy_era'
    mock_time = aware_utc(datetime(2020, 1, 1, 14, 30))
    mock_action = EraAction(url=url,
                            method='POST',
                            payload=dict(resposta=42))
    obj = EventReminderAssistant(mock_name, mock_time, mock_action)
    generic_serialize_roundtrip_test(EventReminderAssistant, obj)


def test_era_serialization_no_payload(url):
    mock_name = 'dummy_era'
    mock_time = aware_utc(datetime(2020, 1, 1, 14, 30))
    mock_action = EraAction(url=url,
                            method='POST')
    obj = EventReminderAssistant(mock_name, mock_time, mock_action)
    generic_serialize_roundtrip_test(EventReminderAssistant, obj)


def test_era_factory():
    mock_name = MagicMock()
    mock_event_time = MagicMock()
    mock_action = MagicMock()
    mock_persist_adapter = MagicMock()
    mock_scheduler_adapter = MagicMock()

    result = era_factory(
        name=mock_name,
        event_time=mock_event_time,
        action=mock_action,
        persist_adapter=mock_persist_adapter,
        scheduler_adapter=mock_scheduler_adapter,
    )

    assert isinstance(result, EventReminderAssistant)
    assert result.name == mock_name
    assert result.event_time == mock_event_time
    assert result.action == mock_action
    assert result.adapter == mock_persist_adapter
    assert result.scheduler_adapter == mock_scheduler_adapter


def test_extend_dict():
    x = {'a': 1}
    y = _extend_dict(x, dict(b=2))
    assert y == dict(a=1, b=2)


# Tests EraRunner
@fixture(scope='class')
def era_runner_factory(request):
    Runner = namedtuple(
        'Runner',
        'era_runner, mock_era_id, mock_scheduler_adapter,'
        'mock_persist_adapter')

    def factory(era_id=MagicMock(),
                scheduler_adapter=MagicMock(),
                persist_adapter=MagicMock()):

        era_runner = EraRunner(era_id=era_id,
                               scheduler_adapter=scheduler_adapter,
                               persist_adapter=persist_adapter)

        return Runner(era_runner, era_id, scheduler_adapter,
                      persist_adapter)

    request.cls.runner_factory = factory


@pytest.mark.usefixtures('era_runner_factory')
class TestEraRunner(TestCase):

    @patch.object(EraRunner, '_execute_action')
    @patch.object(EraRunner, '_remove_current')
    @patch.object(EraRunner, '_setup_next')
    def test_run(self, mock_execute_action, mock_remove_current,
                 mock_setup_next):
        runner: EraRunner = self.runner_factory().era_runner
        runner.run()
        mock_execute_action.assert_called_once()
        mock_remove_current.assert_called_once()
        mock_setup_next.assert_called_once()

    @patch.object(EventReminderAssistant, 'set_adapter')
    @patch.object(EventReminderAssistant, 'set_scheduler_adapter')
    @patch.object(EventReminderAssistant, 'set_scheduler')
    def test_set_up_next(self, mock_set_adapter, mock_set_scheduler_adapter,
                         mock_set_scheduler):
        persist_adapter_mock = MagicMock()
        persist_adapter_mock.filter = MagicMock(
            return_value=[EventReminderAssistant(MagicMock(),
                          MagicMock(), MagicMock())])
        runner = EraRunner(era_id=MagicMock(),
                           scheduler_adapter=MagicMock(),
                           persist_adapter=persist_adapter_mock)

        runner._setup_next()

        mock_set_adapter.assert_called_once()
        mock_set_scheduler_adapter.assert_called_once()
        mock_set_scheduler.assert_called_once()
