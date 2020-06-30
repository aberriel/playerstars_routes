import logging
from aspectlib import Aspect, Proceed, Return


default_logger = logging.getLogger('log-aspect')


class Logging:
    class __Logging:
        def __init__(self):
            log_format = "%(levelname)s %(asctime)s - %(message)s"
            fhandler = logging.FileHandler('log-aspect.log')
            fhandler.setFormatter(logging.Formatter(log_format))
            default_logger.addHandler(fhandler)

            self.logger = default_logger

        def set_logger(self, external_logger):
            self.logger = external_logger

    instance = None

    def __init__(self):
        if not Logging.instance:
            Logging.instance = Logging.__Logging()

    def __getattr__(self, name):
        return getattr(self.instance, name)


@Aspect(bind=True)
def logger_aspect(cutpoint, *args, **kwargs):
    logger = Logging().logger
    name = '{}.{}'.format(cutpoint.__module__, cutpoint.__name__)
    logger.info('Call {}({}, {})'.format(name, args, kwargs))
    try:
        fresult = yield Proceed(*args, **kwargs)

        if fresult:
            logger.info('{} returning {}'.format(name, fresult))

        yield Return(fresult)
    except Exception as exc:
        logger.error('Calling {}({}, {}): {}'.format(name,
                                                     args,
                                                     kwargs,
                                                     exc))
        raise exc
