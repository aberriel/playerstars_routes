from unittest.mock import MagicMock

from pytest import raises

from chalicelib.aspect.logging import Logging, logger_aspect


def test_set_logger():
    logger = Logging()
    mock_logger = MagicMock()

    logger.set_logger(mock_logger)

    assert logger.logger == mock_logger


def test_logger_aspect():
    logger = Logging()
    mock_logger = MagicMock()
    logger.set_logger(mock_logger)

    @logger_aspect
    def mock_func(int_a, int_b):
        return int_a + int_b

    mock_func(2, 5)

    mock_logger.info.assert_called()


def test_logger_aspect_raises():
    logger = Logging()
    mock_logger = MagicMock()
    logger.set_logger(mock_logger)

    @logger_aspect
    def mock_func(int_a, int_b):
        raise ValueError('oops')

    with raises(ValueError) as excinfo:
        mock_func(2, 5)

    mock_logger.info.assert_called()
    assert str(excinfo.value) == 'oops'
