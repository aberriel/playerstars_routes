from collections import namedtuple
from datetime import datetime
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

import pytest
from clapy_basic_classes.basic_domain.util import \
    generic_serialize_roundtrip_test
from playerstars_domain.utils.datetime_helper import aware_utc
from pytest import raises, fixture

from chalicelib.era_labs import BasicTaskSchedulerAdapter, TaskSchedulerPort, \
    AwsTaskSchedulerAdapter, TaskNotFoundException, EventReminderAssistant, \
    era_factory, EraAction, _extend_dict


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


@fixture(scope='class')
def atsa_factory(request):
    Atsa = namedtuple('Atsa', 'atsa, mock_name, mock_ident, mock_exec_time, '
                              'mock_runner')

    def factory(name=MagicMock(),
                identifier=MagicMock(),
                exec_time=MagicMock(),
                runner=MagicMock()):
        atsa = AwsTaskSchedulerAdapter(
            name=name,
            task_id=identifier,
            execution_time=exec_time,
            lambda_runner=runner)
        return Atsa(atsa, name, identifier, exec_time, runner)

    request.cls.atsa_factory = factory


prefix = 'chalicelib.era_labs'


@pytest.mark.usefixtures('atsa_factory')
class TestAtsa(TestCase):
    def setUp(self):
        self.boto_patcher = patch(f'{prefix}.boto3')
        self.mock_boto = self.boto_patcher.start()

    def tearDown(self):
        self.boto_patcher.stop()

    @patch.object(AwsTaskSchedulerAdapter, '_set')
    def test_set(self, mock_set):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_task_id = MagicMock()
        mock_exec_time = MagicMock()
        atsa.set(mock_task_id, mock_exec_time)

        mock_set.assert_called_once()

    @patch.object(AwsTaskSchedulerAdapter, '_delete')
    @patch.object(AwsTaskSchedulerAdapter, '_set')
    def test_update(self, mock_set, mock_delete):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_task_id = MagicMock()
        mock_exec_time = MagicMock()
        atsa.update(mock_task_id, mock_exec_time)

        mock_delete.assert_called_once()
        mock_set.assert_called_once()

    @patch.object(AwsTaskSchedulerAdapter, '_delete')
    def test_delete(self, mock_delete):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.delete()
        mock_delete.assert_called_once()

    def test_datetime_from_cron_expression(self):
        cron_expression = 'cron(45 9 16 8 ? 2020)'
        result = AwsTaskSchedulerAdapter._datetime_from_cron_expression(
            cron_expression)

        expected = aware_utc(datetime(2020, 8, 16, 9, 45, 0))
        self.assertEqual(result, expected)

    def test_get_target(self):
        mock_ev = MagicMock()
        mock_name = MagicMock()
        result = AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        mock_ev.list_targets_by_rule.assert_called_with(Rule=mock_name)

        mock_list_result = mock_ev.list_targets_by_rule()
        mock_list_result.__getitem__.assert_called_with('Targets')

        mock_targets = mock_list_result.__getitem__()
        mock_targets.__getitem__.assert_called_with(0)

        self.assertEqual(result, mock_targets.__getitem__())

    def test_get_target_key_not_found(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(return_value={}))
        mock_name = MagicMock()

        with raises(TaskNotFoundException) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'Key "Targets" not found')

    def test_get_target_error(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(
            side_effect=ValueError('error')))
        mock_name = MagicMock()

        with raises(ValueError) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'error')

    def test_get_target_empty_targets(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(
            return_value={'Targets': []}))
        mock_name = MagicMock()

        with raises(TaskNotFoundException) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'Empty target list found')

    def test_get_identifier_from_target(self):
        mock_target = {'Input': '{"task_id": "Ident"}', 'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter._get_identifier_from_target(
            mock_target)
        assert result == 'Ident'

    def test_get_runner_from_target(self):
        mock_target = {'Input': '{"identifier": "asdf"}', 'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter._get_runner_from_target(
            mock_target)
        assert result == 'meu id'

    @patch.object(AwsTaskSchedulerAdapter, '_datetime_from_cron_expression')
    def test_get_exectime(self, mock_datetime_from_cron):
        mock_ev = MagicMock()
        mock_name = MagicMock()
        result = AwsTaskSchedulerAdapter._get_exectime(mock_ev, mock_name)

        mock_ev.describe_rule.assert_called_with(Name=mock_name)
        mock_rule = mock_ev.describe_rule()
        mock_rule.__getitem__.assert_called_with('ScheduleExpression')
        mock_expression = mock_rule.__getitem__()
        mock_datetime_from_cron.assert_called_with(mock_expression)

        self.assertEqual(result, mock_datetime_from_cron())

    @patch.object(AwsTaskSchedulerAdapter, '_get_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_init_events_client')
    @patch.object(AwsTaskSchedulerAdapter, '_get_identifier_from_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_runner_from_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_exectime')
    def test_get_current(self,
                         mock_get_exectime,
                         mock_get_runner,
                         mock_get_ident,
                         mock_get_ev,
                         mock_get_target):
        mock_name = MagicMock()
        mock_get_target.return_value = {'Input': '{"identifier": "asdf"}',
                                        'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter.get_current(mock_name)

        mock_get_target.assert_called_with(mock_get_ev(), mock_name)
        mock_get_ident.assert_called_with(mock_get_target())
        mock_get_runner.assert_called_with(mock_get_target())
        mock_get_exectime.assert_called_with(mock_get_ev(), mock_name)

        self.assertIsInstance(result, AwsTaskSchedulerAdapter)

        self.assertEqual(result.name, mock_name)
        self.assertEqual(result.task_id, mock_get_ident())
        self.assertEqual(result.execution_time, mock_get_exectime())
        self.assertEqual(result.lambda_runner, mock_get_runner())

    @patch.object(AwsTaskSchedulerAdapter, '_put_rule')
    @patch.object(AwsTaskSchedulerAdapter, '_put_targets')
    @patch.object(AwsTaskSchedulerAdapter, 'make_stmt_id')
    @patch.object(AwsTaskSchedulerAdapter, '_add_permission')
    def test__set(self,
                  mock_add_permission,
                  mock_make_stmt,
                  mock_put_targets,
                  mock_put_rule):
        atsa = self.atsa_factory().atsa

        atsa._set()
        mock_put_rule.assert_called_once()
        mock_put_targets.assert_called_once()
        mock_make_stmt.assert_called_with(mock_put_rule())
        mock_add_permission.assert_called_with(mock_make_stmt(),
                                               mock_put_rule())

    @patch.object(AwsTaskSchedulerAdapter, '_remove_permission')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_targets')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_rule')
    @patch.object(AwsTaskSchedulerAdapter, '_get_rule_arn')
    @patch.object(AwsTaskSchedulerAdapter, 'make_stmt_id')
    def test__delete(self,
                     mock_make_stmt,
                     mock_get_rule,
                     mock_remove_rule,
                     mock_remove_targets,
                     mock_remove_permission):
        atsa = self.atsa_factory().atsa

        atsa._delete()

        mock_get_rule.assert_called_once()
        mock_make_stmt.assert_called_with(mock_get_rule())
        mock_remove_permission.assert_called_with(mock_make_stmt())
        mock_remove_targets.assert_called_once()
        mock_remove_rule.assert_called_once()

    def test_make_cron_expression(self):
        mock_date = datetime(2020, 1, 2, 3, 4)
        result = AwsTaskSchedulerAdapter._make_cron_expression(mock_date)

        self.assertEqual(result, 'cron(4 3 2 1 ? 2020)')

    def test_get_lambda_function_arn(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa.lambda_client.get_function_configuration = MagicMock(
            return_value={'FunctionArn': 'fnconfig'})

        result = atsa._get_lambda_function_arn()

        atsa.lambda_client.get_function_configuration.assert_called_with(
            FunctionName=atsa.lambda_runner)

        self.assertEqual(result, 'fnconfig')

    @patch.object(AwsTaskSchedulerAdapter, '_make_cron_expression')
    def test_put_rule(self, mock_make_cron):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_put_rule = MagicMock(return_value={'RuleArn': 'the rule arn!'})
        atsa.events_client.put_rule = mock_put_rule
        mock_exec_time = MagicMock()
        result = atsa._put_rule(mock_exec_time)

        mock_put_rule.assert_called_with(Name=atsa.name,
                                         ScheduleExpression=mock_make_cron())

        self.assertEqual(result, 'the rule arn!')

    @patch.object(AwsTaskSchedulerAdapter, '_make_targets')
    def test_put_targets(self, mock_make_targets):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa.events_client = MagicMock()
        result = atsa._put_targets()

        atsa.events_client.put_targets.assert_called_with(
            Rule=atsa.name,
            Targets=mock_make_targets()
        )
        self.assertEqual(result, atsa.events_client.put_targets())

    @patch.object(AwsTaskSchedulerAdapter, '_get_lambda_function_arn')
    def test_make_targets(self, mock_glfa):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory(
            identifier='sou eu').atsa

        atsa.name = 'scheduler_name'
        result = atsa._make_targets()

        mock_glfa.assert_called_once()

        expected = [{
            'Id': atsa.lambda_runner,
            'Arn': mock_glfa(),
            'Input': '{"scheduler_name": "scheduler_name", "era_id": "sou eu"}'
        }]

        self.assertEqual(result, expected)

    def test_make_stmt_id(self):
        result = AwsTaskSchedulerAdapter.make_stmt_id('um role arn qualquer')
        self.assertEqual(result, '13ad085fd6c4e295090a8238d852d1ea'
                                 '2af5b5f618efbf7255c48ad9de0507e4')

    def test__get_policy_statement_ids(self):
        mock_policy = dict(Policy='{"Statement": [{"Sid": 1}, {"Sid": 2}]}')
        result = AwsTaskSchedulerAdapter._get_policy_statement_ids(mock_policy)

        self.assertListEqual(result, [1, 2])

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    def test_clear_permissions(self, mock_remove_policies, mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa._clear_permissions()

        mock_get_policy.assert_called_once()
        mock_remove_policies.assert_called_with(mock_get_policy())

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy',
                  side_effect=ValueError('nada'))
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    @patch.object(AwsTaskSchedulerAdapter, '_is_resource_not_found_exception',
                  return_value=True)
    def test_clear_permissions_empty(self,
                                     mock_is_resource_not_found,
                                     mock_remove_policies,
                                     mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa._clear_permissions()

        mock_is_resource_not_found.assert_called_once()
        mock_get_policy.assert_called_once()
        mock_remove_policies.assert_not_called()

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy',
                  side_effect=ValueError('Erro mesmo'))
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    @patch.object(AwsTaskSchedulerAdapter, '_is_resource_not_found_exception',
                  return_value=False)
    def test_clear_permissions_error(self,
                                     mock_is_resource_not_found,
                                     mock_remove_policies,
                                     mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        with raises(ValueError) as excinfo:
            atsa._clear_permissions()

        self.assertEqual(str(excinfo.value), 'Erro mesmo')

    def test_is_resource_not_found_exception(self):
        mock = MagicMock(
            __class__=MagicMock(
                __name__='ResourceNotFoundException'))
        result = AwsTaskSchedulerAdapter._is_resource_not_found_exception(mock)
        self.assertTrue(result)

    def test_not_is_resource_not_found_exception(self):
        mock = ValueError('oops')
        result = AwsTaskSchedulerAdapter._is_resource_not_found_exception(mock)
        self.assertFalse(result)

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy_statement_ids',
                  return_value=[17, 42])
    def test_remove_policies(self, mock_gpsi):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_policies = MagicMock()
        atsa.lambda_client = MagicMock()
        atsa._remove_policies(mock_policies)

        mock_gpsi.assert_called_with(mock_policies)

        atsa.lambda_client.remove_permission.assert_has_calls(
            [call(FunctionName=atsa.lambda_runner, StatementId=17),
             call(FunctionName=atsa.lambda_runner, StatementId=42)])

    def test__get_policy(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        result = atsa._get_policy()

        atsa.lambda_client.get_policy.assert_called_with(
            FunctionName=atsa.lambda_runner)

        self.assertEqual(result, atsa.lambda_client.get_policy())

    @patch.object(AwsTaskSchedulerAdapter, '_clear_permissions')
    def test__add_permission(self, mock_clear_permission):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        mock_stmt_id = MagicMock()
        mock_rule_arn = MagicMock()
        atsa._add_permission(mock_stmt_id, mock_rule_arn)

        mock_clear_permission.assert_called_once()
        atsa.lambda_client.add_permission.assert_called_with(
            Action='lambda:InvokeFunction',
            FunctionName=atsa.lambda_runner,
            Principal='events.amazonaws.com',
            SourceArn=mock_rule_arn,
            StatementId=mock_stmt_id
        )

    def test__remove_permission(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        mock_stmt = MagicMock()
        atsa._remove_permission(mock_stmt)
        atsa.lambda_client.remove_permission.assert_called_with(
            FunctionName=atsa.lambda_runner,
            StatementId=mock_stmt
        )

    def test__remove_targets(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        atsa._remove_targets()

        atsa.events_client.remove_targets.assert_called_with(
            Rule=atsa.name,
            Ids=[atsa.lambda_runner])

    def test__remove_rule(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        atsa._remove_rule()
        atsa.events_client.delete_rule.assert_called_with(Name=atsa.name)

    def test__get_rule_arn(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        result = atsa._get_rule_arn()
        atsa.events_client.describe_rule.assert_called_with(Name=atsa.name)
        mock_describe_rule = atsa.events_client.describe_rule()
        mock_describe_rule.__getitem__.assert_called_with('Arn')
        assert result == mock_describe_rule.__getitem__()


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


@patch.object(EventReminderAssistant, '_set_scheduler')
def test_era_save(mock_set_scheduler, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era

    era.save()

    fac.mock_persist_adapter.save.assert_called_once()
    mock_set_scheduler.assert_called_once()


@patch.object(EventReminderAssistant, '_update_if_sooner')
def test_set_scheduler(mock_update_if_sooner, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era

    era._set_scheduler()

    mock_update_if_sooner.assert_called_once()


@patch.object(EventReminderAssistant, '_set_scheduler')
def test_set_scheduler(mock_set_scheduler, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era

    era.set_scheduler()

    mock_set_scheduler.assert_called_once()


@patch.object(EventReminderAssistant, '_update_if_sooner',
              side_effect=TaskNotFoundException('olá!'))
def test_set_scheduler_create(mock_update_if_sooner, era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era

    era._set_scheduler()

    mock_update_if_sooner.assert_called_once()
    fac.mock_scheduler_adapter.set.assert_called_once()


@patch.object(EventReminderAssistant, '_get_current_scheduler',
              return_value=MagicMock(
                  execution_time=datetime(2020, 8, 22, 10, 0)))
def test_update_if_sooner_no_update(mock_get_current_scheduler,
                                    era_factory_fixture):
    mock_our_exec_time = datetime(2020, 8, 22, 10, 1)

    fac: Factory = era_factory_fixture(mock_event_time=mock_our_exec_time)
    era: EventReminderAssistant = fac.era

    era._update_if_sooner()

    mock_get_current_scheduler.assert_called_once()
    mock_current = mock_get_current_scheduler()
    assert mock_current.execution_time == datetime(2020, 8, 22, 10, 0)
    fac.mock_scheduler_adapter.update.assert_not_called()


@patch.object(EventReminderAssistant, '_get_current_scheduler',
              return_value=MagicMock(
                  execution_time=datetime(2020, 8, 22, 10, 1)))
def test_update_if_sooner_update(mock_get_current_scheduler,
                                 era_factory_fixture):
    mock_our_exec_time = datetime(2020, 8, 22, 10, 0)

    fac: Factory = era_factory_fixture(mock_event_time=mock_our_exec_time)
    era: EventReminderAssistant = fac.era

    era._update_if_sooner()

    mock_get_current_scheduler.assert_called_once()
    fac.mock_scheduler_adapter.update.assert_called_once()


def test_get_current_scheduler(era_factory_fixture):
    fac: Factory = era_factory_fixture()
    era: EventReminderAssistant = fac.era

    result = era._get_current_scheduler()

    fac.mock_scheduler_adapter.get_current.assert_called_with(
        fac.mock_scheduler_adapter.name)
    assert result == fac.mock_scheduler_adapter.get_current()


def test_get_task_id():
    assert AwsTaskSchedulerAdapter.get_task_id_name() == 'task_id'


def test_extend_dict():
    x = {'a': 1}
    y = _extend_dict(x, dict(b=2))
    assert y == dict(a=1, b=2)
