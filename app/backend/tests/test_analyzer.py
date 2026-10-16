import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from openai import APIConnectionError, APIStatusError, APITimeoutError, RateLimitError

from core.config import get_settings
from services import analyzer
from models import Submission
from error_types import ErrorType
from tests.test_review import RESULT, REQUEST


@pytest.fixture
def ai(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-only-key')
    get_settings.cache_clear()
    create = AsyncMock(return_value=SimpleNamespace(choices=[SimpleNamespace(
        finish_reason='stop', message=SimpleNamespace(content=json.dumps(RESULT)),
    )]))
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    context = AsyncMock()
    context.__aenter__.return_value = client
    factory = Mock(return_value=context)
    monkeypatch.setattr(analyzer, 'AsyncOpenAI', factory)
    yield create, factory
    get_settings.cache_clear()


def test_validated_analysis_and_policy(client, auth, ai):
    create, factory = ai
    assert client.post('/review/analyze', headers=auth, json=REQUEST).status_code == 200
    assert factory.call_args.kwargs['timeout'] == 30
    assert factory.call_args.kwargs['max_retries'] == 2
    prompt = create.call_args.kwargs['messages'][0]['content']
    assert all(category.value in prompt for category in ErrorType)


@pytest.mark.parametrize('content', [
    'invalid JSON', '{}', json.dumps({**RESULT, 'summary': 123}),
    json.dumps({**RESULT, 'weaknesses': [{'type': 'Invented', 'line': 1, 'explanation': 'x'}]}),
    json.dumps({**RESULT, 'weaknesses': [{'type': 'LogicError', 'line': '1', 'explanation': 'x'}]}),
    json.dumps({**RESULT, 'weaknesses': [{'type': 'LogicError', 'line': -1, 'explanation': 'x'}]}),
    json.dumps({**RESULT, 'summary': 'x' * 2001}), None,
])
def test_invalid_ai_never_persisted(client, auth, db, ai, content, caplog):
    ai[0].return_value.choices[0].message.content = content
    response = client.post('/review/analyze', headers=auth, json=REQUEST)
    assert response.status_code == 502
    assert db.query(Submission).count() == 0
    assert 'test-only-key' not in caplog.text


@pytest.mark.parametrize('kind,status', [('timeout',503), ('connection',503), ('rate',503), ('server',503), ('auth',502), ('unexpected',500)])
def test_upstream_error_mapping(client, auth, db, ai, kind, status, caplog):
    request = httpx.Request('POST', 'https://api.openai.com/v1/chat/completions')
    if kind == 'timeout':
        error = APITimeoutError(request=request)
    elif kind == 'connection':
        error = APIConnectionError(request=request)
    elif kind == 'unexpected':
        error = RuntimeError('private code and secret key')
    else:
        code = {'rate':429, 'server':500, 'auth':401}[kind]
        cls = RateLimitError if kind == 'rate' else APIStatusError
        error = cls('private code and secret key', response=httpx.Response(code, request=request), body=None)
    ai[0].side_effect = error
    assert client.post('/review/analyze', headers=auth, json=REQUEST).status_code == status
    assert db.query(Submission).count() == 0
    assert 'private code and secret key' not in caplog.text


def test_unconfigured_ai_returns_503(client, auth, monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    get_settings.cache_clear()
    assert client.post('/review/analyze', headers=auth, json=REQUEST).status_code == 503
    get_settings.cache_clear()


@pytest.mark.parametrize('kind', ['truncated', 'no-choices', 'refusal'])
def test_incomplete_responses_rejected(client, auth, db, ai, kind):
    if kind == 'no-choices':
        ai[0].return_value.choices = []
    else:
        ai[0].return_value.choices[0].finish_reason = 'length' if kind == 'truncated' else 'content_filter'
    assert client.post('/review/analyze', headers=auth, json=REQUEST).status_code == 502
    assert db.query(Submission).count() == 0
