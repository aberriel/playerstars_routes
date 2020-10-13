from copy import deepcopy
from datetime import datetime
from logging import getLogger

import requests
from clapy_basic_classes.basic_persist_adapter import BasicPersistAdapter
from playerstars_domain.utils.datetime_helper import aware_now
from playerstars_domain import EventReminderAssistant, EraAction
from clapy_basic_classes.basic_domain.task_scheduler_port import\
    TaskSchedulerPort
from clapy_basic_classes.basic_scheduler_adapter.basic_scheduler_adapter \
    import BasicTaskSchedulerAdapter


def era_factory(name: str,
                event_time: datetime,
                action: EraAction,
                persist_adapter: BasicPersistAdapter,
                scheduler_adapter: BasicTaskSchedulerAdapter):
    era = EventReminderAssistant(name=name,
                                 event_time=event_time,
                                 action=action)
    era.set_adapter(persist_adapter)
    era.set_scheduler_adapter(scheduler_adapter)
    return era

# Era Runner


def _extend_dict(a_dict: dict, extension: dict):
    result = deepcopy(a_dict)
    result.update(extension)
    return result


class EraRunner(TaskSchedulerPort):
    def __init__(self,
                 era_id: str,
                 scheduler_adapter: BasicTaskSchedulerAdapter,
                 persist_adapter: BasicPersistAdapter,
                 logger=None):
        super().__init__()
        self.era_id = era_id
        self.logger = logger or getLogger(__name__)
        self.set_scheduler_adapter(scheduler_adapter)
        self.persist_adapter = persist_adapter

    def run(self):
        current_era = self._execute_action()

        self._remove_current(current_era)
        try:
            self._setup_next()
        except Exception as e:
            self.logger.info(f'Error ao setar próximo ERA: {str(e)} ...')

    def _remove_current(self, current_era: EventReminderAssistant):
        current_era.set_scheduler_adapter(self.scheduler_adapter)
        current_era.delete()

    def _execute_action(self):
        self.logger.info(f'Executando {self.era_id}...')
        era: EventReminderAssistant = self.persist_adapter.get_by_id(
            self.era_id)
        era.set_adapter(self.persist_adapter)
        era.set_scheduler_adapter(self.scheduler_adapter)

        args = {'url': era.action.url}
        args_with_payload = _extend_dict(args, {'data': era.action.payload})
        map_request = {
            'GET': (requests.get, args),
            'DELETE': (requests.delete, args),
            'POST': (requests.post, args_with_payload),
            'PUT': (requests.put, args_with_payload)
        }
        fn, fn_args = map_request[era.action.method]
        response = fn(**fn_args)

        self._log_response(response)

        return era

    def _log_response(self, response):
        now = aware_now().isoformat()
        try:
            report = response.json()
        except Exception:
            report = 'None'

        self.logger.info(f'{now}: ERA Execution: {report}')

    def _setup_next(self):
        now = aware_now().isoformat()
        all_eras = self.persist_adapter.filter(event_time__gte=now)

        if len(all_eras) == 0:
            return

        oredered_eras = sorted(all_eras, key=lambda x: x.event_time)
        next_era_type = type(oredered_eras[0]).__name__
        self.logger.info(f'Next Era {next_era_type}: '
                         f'{oredered_eras[0].entity_id}...')
        next_era: EventReminderAssistant = oredered_eras[0]

        next_era.set_adapter(self.persist_adapter)
        next_era.set_scheduler_adapter(self.scheduler_adapter)
        next_era.set_scheduler()
