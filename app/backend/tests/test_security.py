from datetime import timedelta

import pytest
from pydantic import ValidationError
from jose import jwt

from core.config import Settings, get_settings
from core.security import create_access_token
from models import Submission, Weakness


def test_missing_secret_fails_fast(monkeypatch):
    monkeypatch.delenv('SECRET_KEY')
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


@pytest.mark.parametrize('secret', ['', 'short', 'super_secret_key_needs_to_be_changed'])
def test_unsafe_secret_rejected(secret):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, secret_key=secret)


def test_dashboard_bound_to_authenticated_user(client, db, users, auth):
    alice, bob = users
    for owner, category in [(alice, 'LogicError'), (bob, 'Security')]:
        submission = Submission(owner_id=owner.id, code_snippet='x', language='python', summary='summary')
        submission.weaknesses.append(Weakness(type=category, explanation='detail'))
        db.add(submission)
    db.commit()
    assert client.get('/dashboard/stats/me').status_code == 401
    response = client.get('/dashboard/stats/me', headers=auth)
    assert response.json() == {'total_submissions': 1, 'stats': [{'weakness_type': 'LogicError', 'count': 1}]}
    assert client.get('/dashboard/stats/bob', headers=auth).status_code == 404
    assert client.get('/dashboard/stats/me?user_id=bob', headers=auth).json() == response.json()


@pytest.mark.parametrize('token', ['broken', 'expired', 'no-exp', 'wrong-key'])
def test_invalid_tokens(client, users, token):
    if token == 'expired':
        token = create_access_token({'sub': 'alice'}, timedelta(seconds=-1))
    elif token == 'no-exp':
        token = jwt.encode({'sub': 'alice'}, get_settings().secret_key.get_secret_value(), algorithm='HS256')
    elif token == 'wrong-key':
        token = jwt.encode({'sub': 'alice', 'exp': 9999999999}, 'wrong-signature-key', algorithm='HS256')
    assert client.get('/dashboard/stats/me', headers={'Authorization': f'Bearer {token}'}).status_code == 401


def test_inactive_user_rejected(client, db, users, auth):
    users[0].is_active = 0
    db.commit()
    assert client.get('/dashboard/stats/me', headers=auth).status_code == 401
    assert client.post('/auth/login', data={'username': 'alice', 'password': 'password123'}).status_code == 401
