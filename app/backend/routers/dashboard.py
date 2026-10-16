from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

import database
import models
import schemas
from dependencies import get_current_user

router = APIRouter(prefix='/dashboard', tags=['Dashboard'])


@router.get('/stats/me', response_model=schemas.DashboardResponse)
def get_user_stats(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    total = db.query(models.Submission).filter(models.Submission.owner_id == current_user.id).count()
    results = (
        db.query(models.Weakness.type, func.count(models.Weakness.id).label('count'))
        .join(models.Submission)
        .filter(models.Submission.owner_id == current_user.id)
        .group_by(models.Weakness.type)
        .order_by(func.count(models.Weakness.id).desc(), models.Weakness.type)
        .all()
    )
    return schemas.DashboardResponse(
        total_submissions=total,
        stats=[schemas.StatItem(weakness_type=category, count=count) for category, count in results],
    )
