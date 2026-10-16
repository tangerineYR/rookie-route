from unittest.mock import AsyncMock

import pytest
from sqlalchemy import event, text
from sqlalchemy.exc import DBAPIError, IntegrityError, StatementError

from models import Submission, Weakness, User
from schemas import AIAnalysisResult
from routers import review

RESULT = {'summary': '문제 발견', 'weaknesses': [{'type': 'LogicError', 'line': 1, 'explanation': '조건 확인'}]}
REQUEST = {'code': 'print(1)', 'language': 'python'}


@pytest.fixture
def analyzer(monkeypatch):
    mock = AsyncMock(return_value=AIAnalysisResult.model_validate(RESULT))
    monkeypatch.setattr(review, 'call_openai_analyzer', mock)
    return mock


def test_analysis_persists_and_dashboard(client, db, users, auth, analyzer):
    assert client.post('/review/analyze', json=REQUEST).status_code == 401
    response = client.post('/review/analyze', json=REQUEST, headers=auth)
    assert response.status_code == 200
    assert response.json()['weaknesses'] == RESULT['weaknesses']
    submission = db.query(Submission).one()
    assert submission.owner_id == users[0].id
    assert db.query(Weakness).one().submission_id == submission.id
    assert client.get('/dashboard/stats/me', headers=auth).json()['total_submissions'] == 1


def test_weakness_failure_rolls_back_submission(client, db, auth, analyzer, caplog):
    def reject(mapper, connection, target):
        raise IntegrityError('private source', {}, Exception('secret credential'))
    event.listen(Weakness, 'before_insert', reject)
    try:
        response = client.post('/review/analyze', json=REQUEST, headers=auth)
    finally:
        event.remove(Weakness, 'before_insert', reject)
    assert response.status_code == 500
    assert db.query(Submission).count() == db.query(Weakness).count() == 0
    assert 'private source' not in caplog.text
    assert 'secret credential' not in caplog.text


def test_invalid_input_never_calls_ai(client, auth, analyzer):
    assert client.post('/review/analyze', json={**REQUEST, 'code': 'x' * 15001}, headers=auth).status_code == 422
    analyzer.assert_not_awaited()


@pytest.mark.parametrize('delete_user', [False, True])
def test_database_cascade(db, users, delete_user):
    submission = Submission(owner_id=users[0].id, code_snippet='x', language='python')
    submission.weaknesses = [Weakness(type='Other', explanation='detail')]
    db.add(submission)
    db.commit()
    # Bulk SQL deletion exercises ON DELETE rather than only ORM cascades.
    if delete_user:
        db.query(User).filter(User.id == users[0].id).delete()
    else:
        db.query(Submission).filter(Submission.id == submission.id).delete()
    db.commit()
    assert db.query(Submission).count() == 0
    assert db.query(Weakness).count() == 0


def test_orphan_removal_and_category_validation(db, users):
    submission = Submission(owner_id=users[0].id, code_snippet='x', language='python')
    submission.weaknesses = [Weakness(type='Other', explanation='detail')]
    db.add(submission)
    db.commit()
    submission.weaknesses.clear()
    db.commit()
    assert db.query(Weakness).count() == 0
    db.add(Weakness(submission_id=submission.id, type='Invented', explanation='detail'))
    with pytest.raises(StatementError):
        db.commit()
    db.rollback()
    with pytest.raises(DBAPIError) as error:
        db.execute(text("INSERT INTO weaknesses (submission_id, type, explanation) VALUES (:id, 'Invented', 'x')"), {'id': submission.id})
    assert 'error_type' in str(error.value.orig)
    db.rollback()
