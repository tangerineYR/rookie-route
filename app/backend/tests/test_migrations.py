import os
from pathlib import Path
import subprocess
import sys

import pytest
from sqlalchemy import create_engine, inspect, MetaData, text

BACKEND = Path(__file__).resolve().parents[1]


@pytest.fixture
def migration_db(tmp_path):
    url = os.environ.get('MIGRATION_TEST_DATABASE_URL', f'sqlite:///{tmp_path / "migration.db"}')
    if not url.startswith('sqlite:') and not url.endswith('/rookie_route_migration_test'):
        raise RuntimeError('Migration tests require dedicated rookie_route_migration_test database')
    engine = create_engine(url)
    def clean():
        metadata = MetaData()
        metadata.reflect(engine)
        metadata.drop_all(engine)
    clean()
    yield engine, {**os.environ, 'DATABASE_URL': url}
    clean()
    engine.dispose()


def migrate(env, *args, success=True):
    result = subprocess.run(
        [sys.executable, '-m', 'alembic', *args], cwd=BACKEND, env=env,
        text=True, capture_output=True,
    )
    if success:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0
    return result


def seed(engine, orphan=False, category='LogicError'):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO users (id, username, email, hashed_password, is_active) VALUES (1, 'alice', 'alice@example.com', 'hash', 1)"))
        conn.execute(text("INSERT INTO submissions (id, user_id, code_snippet, language, summary) VALUES (1, :owner, 'print(1)', 'python', 'summary')"), {'owner': 'missing' if orphan else 'alice'})
        conn.execute(text("INSERT INTO weaknesses (id, submission_id, user_id, type, line, explanation) VALUES (1, 1, :owner, :category, 1, 'detail')"), {'owner': 'missing' if orphan else 'alice', 'category': category})


def test_fresh_migrations_match_models(migration_db):
    engine, env = migration_db
    migrate(env, 'upgrade', 'head')
    migrate(env, 'check')
    assert 'owner_id' in {c['name'] for c in inspect(engine).get_columns('submissions')}
    migrate(env, 'downgrade', 'base')
    migrate(env, 'upgrade', 'head')
    migrate(env, 'check')


def test_legacy_backfill_roundtrip(migration_db):
    engine, env = migration_db
    migrate(env, 'upgrade', '0001')
    seed(engine)
    migrate(env, 'upgrade', 'head')
    with engine.connect() as conn:
        assert conn.scalar(text('SELECT owner_id FROM submissions')) == 1
        assert conn.scalar(text('SELECT explanation FROM weaknesses')) == 'detail'
    migrate(env, 'downgrade', '0001')
    with engine.connect() as conn:
        assert conn.scalar(text('SELECT user_id FROM submissions')) == 'alice'
        assert conn.scalar(text('SELECT user_id FROM weaknesses')) == 'alice'
    migrate(env, 'upgrade', 'head')
    migrate(env, 'check')


@pytest.mark.parametrize('orphan,category', [(True, 'LogicError'), (False, 'Unknown')])
def test_preflight_rejects_invalid_legacy_without_data_loss(migration_db, orphan, category):
    engine, env = migration_db
    migrate(env, 'upgrade', '0001')
    seed(engine, orphan, category)
    migrate(env, 'upgrade', 'head', success=False)
    assert 'owner_id' not in {c['name'] for c in inspect(engine).get_columns('submissions')}
    with engine.connect() as conn:
        assert conn.scalar(text('SELECT COUNT(*) FROM submissions')) == 1
        assert conn.scalar(text('SELECT COUNT(*) FROM weaknesses')) == 1
        assert conn.scalar(text('SELECT version_num FROM alembic_version')) == '0001'
