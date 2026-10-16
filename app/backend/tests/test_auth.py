import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import User

PAYLOAD = {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'password123'}


def test_signup_login_duplicates(client):
    assert client.post('/auth/signup', json=PAYLOAD).status_code == 201
    login = client.post('/auth/login', data={'username': 'charlie', 'password': 'password123'})
    assert login.status_code == 200
    assert login.json()['access_token']
    assert client.post('/auth/signup', json={**PAYLOAD, 'username': 'different'}).status_code == 409
    assert client.post('/auth/signup', json={**PAYLOAD, 'email': 'different@example.com'}).status_code == 409
    assert client.post('/auth/login', data={'username': 'charlie', 'password': 'bad'}).status_code == 401


@pytest.mark.parametrize('changes', [
    {'email': 'bad-email'}, {'username': 'a'}, {'username': 'a' * 51},
    {'password': 'short'}, {'password': '가' * 25},
])
def test_signup_validation(client, changes):
    assert client.post('/auth/signup', json={**PAYLOAD, **changes}).status_code == 422


def test_signup_concurrent_integrity_failure_rolls_back(client, db, monkeypatch):
    def fail_commit(self):
        raise IntegrityError('sensitive sql', {}, Exception('sensitive detail'))
    monkeypatch.setattr(Session, 'commit', fail_commit)
    response = client.post('/auth/signup', json=PAYLOAD)
    assert response.status_code == 409
    assert db.query(User).count() == 0
    assert 'sensitive' not in response.text
