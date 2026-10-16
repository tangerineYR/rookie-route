import json
import logging


class EventFormatter(logging.Formatter):
    """Allowlist fields so provider bodies, SQL parameters and source stay private."""
    def format(self, record):
        event = {
            'level': record.levelname,
            'logger': record.name,
            'event': getattr(record, 'event', record.msg),
        }
        for name in ('error_type', 'status'):
            if hasattr(record, name):
                event[name] = getattr(record, name)
        return json.dumps(event, ensure_ascii=False)


def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(EventFormatter())
    for name in ('services', 'routers'):
        logger = logging.getLogger(name)
        if not any(isinstance(h.formatter, EventFormatter) for h in logger.handlers):
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
