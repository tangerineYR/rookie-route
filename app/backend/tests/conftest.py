import os
import secrets
from pathlib import Path
import sys

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['SECRET_KEY'] = secrets.token_urlsafe(48)
os.environ['DATABASE_URL'] = 'sqlite://'
os.environ.pop('OPENAI_API_KEY', None)

from back_main import app
from database import Base, get_db
from core.security import create_access_token, get_password_hash
from models import User


@pytest.fixture
def engine(tmp_path):
    url = os.environ.get('TEST_DATABASE_URL', f'sqlite:///{tmp_path / "test.db"}')
    if not url.startswith('sqlite:') and not url.endswith('/rookie_route_test'):
        raise RuntimeError('Integration tests require the dedicated rookie_route_test database')
    engine = create_engine(url)
    if engine.dialect.name == 'sqlite':
        event.listen(engine, 'connect', lambda conn, _: conn.execute('PRAGMA foreign_keys=ON'))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db(engine):
    with sessionmaker(bind=engine, autoflush=False)() as session:
        yield session


@pytest.fixture
def client(engine):
    def test_db():
        with sessionmaker(bind=engine, autoflush=False)() as session:
            yield session
    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def users(db):
    result = []
    for name in ['alice', 'bob']:
        user = User(username=name, email=f'{name}@example.com', hashed_password=get_password_hash('password123'))
        db.add(user)
        result.append(user)
    db.commit()
    for user in result:
        db.refresh(user)
    return result


@pytest.fixture
def auth(users, db):
    headers = {'Authorization': 'Bearer ' + create_access_token({'sub': users[0].username})}
    # End the fixture read snapshot before the API writes in another session.
    db.rollback()
    return headers
