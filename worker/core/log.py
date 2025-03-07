import logging

from core.config import settings


def setup_logging() -> None:
    log_format = '%(asctime)s - [%(levelname)s] - [%(name)s:%(lineno)s] - %(message)s'
    logging.basicConfig(
        format=log_format, level=logging.getLevelName(settings.LOG_LEVEL)
    )

    log = logging.getLogger('sqlalchemy.engine.Engine')
    log.handlers.pop()
