import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import database
import models
import schemas
from dependencies import get_current_user
from services.analyzer import call_openai_analyzer

router = APIRouter(prefix='/review', tags=['Code Review'])
logger = logging.getLogger(__name__)


@router.post('/analyze', response_model=schemas.AnalysisResponse)
async def analyze_code(
    request: schemas.CodeRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await call_openai_analyzer(request.code, request.language)
    try:
        submission = models.Submission(
            owner_id=current_user.id, code_snippet=request.code,
            language=request.language, summary=result.summary,
        )
        db.add(submission)
        db.flush()
        db.add_all([
            models.Weakness(submission_id=submission.id, **weakness.model_dump())
            for weakness in result.weaknesses
        ])
        response = schemas.AnalysisResponse(submission_id=submission.id, **result.model_dump())
        db.commit()
        return response
    except SQLAlchemyError as error:
        db.rollback()
        logger.error('analysis_database_failure', extra={
            'event': 'analysis_database_failure', 'error_type': type(error).__name__,
        })
        raise HTTPException(500, 'Failed to save analysis.') from None
    except Exception as error:
        db.rollback()
        logger.error('analysis_unexpected_failure', extra={
            'event': 'analysis_unexpected_failure', 'error_type': type(error).__name__,
        })
        raise HTTPException(500, 'Unexpected analysis failure.') from None
