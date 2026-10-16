import json
import logging

from core.logging import EventFormatter


def test_event_logging_excludes_sensitive_details():
    record = logging.LogRecord('services.analyzer', logging.ERROR, '', 1, 'ai_api_failure', (), None)
    record.event = 'ai_api_failure'
    record.status = 502
    record.source_code = 'private source'
    record.api_key = 'private key'
    output = EventFormatter().format(record)
    assert json.loads(output)['status'] == 502
    assert 'private' not in output
