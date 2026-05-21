import logging
import sys
from pythonjsonlogger import jsonlogger

from app.core.config import settings

logger = logging.getLogger("rag_chat_storage")


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s %(environment)s %(path)s %(error)s")
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL.upper())
