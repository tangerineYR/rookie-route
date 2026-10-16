import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import database
import models
import schemas
from core import security

router = APIRouter(prefix='/auth', tags=['Authentication'])
logger = logging.getLogger(__name__)


@router.post('/signup', response_model=schemas.UserResponse, status_code=201)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        if db.query(models.User).filter(or_(
            models.User.username == user.username, models.User.email == str(user.email),
        )).first():
            raise HTTPException(409, '이미 등록된 사용자명 또는 이메일입니다.')
        new_user = models.User(
            username=user.username, email=str(user.email),
            hashed_password=security.get_password_hash(user.password),
        )
        db.add(new_user)
        db.flush()
        response = schemas.UserResponse.model_validate(new_user)
        db.commit()
        return response
    except IntegrityError:
        # Covers concurrent signups that both pass the initial lookup.
        db.rollback()
        raise HTTPException(409, '이미 등록된 사용자명 또는 이메일입니다.') from None
    except SQLAlchemyError as error:
        db.rollback()
        logger.error('signup_database_failure', extra={'event': 'signup_database_failure', 'error_type': type(error).__name__})
        raise HTTPException(500, 'Failed to create account.') from None


@router.post('/login', response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not user.is_active or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, '아이디 또는 비밀번호가 잘못되었습니다.', headers={'WWW-Authenticate': 'Bearer'})
    return {'access_token': security.create_access_token({'sub': user.username}), 'token_type': 'bearer'}
