import logging
from pythonjsonlogger import jsonlogger


log = logging.getLogger()
formatter = jsonlogger.JsonFormatter(
    "%(levelname)-8s %(name)-12s %(filename)-10s %(lineno)d %(message)s", timestamp=True
)
handler = logging.StreamHandler()
handler.addFilter(lambda record: False if record.getMessage().endswith('/health HTTP/1.1" 200') else True)
handler.addFilter(lambda record: False if record.getMessage().endswith('/ready HTTP/1.1" 200') else True)
handler.setFormatter(formatter)
log.addHandler(handler)


# silence unwanted logs
logging.getLogger("gunicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").handlers = []
