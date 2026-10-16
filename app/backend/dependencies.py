from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import database
import models
from core.config import get_settings
from core.security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='자격 증명을 확인할 수 없습니다.',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token, get_settings().secret_key.get_secret_value(),
            algorithms=[ALGORITHM], options={'require_exp': True, 'require_sub': True},
        )
        username = payload.get('sub')
        if not isinstance(username, str) or not username:
            raise error
    except JWTError:
        raise error from None
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None or not user.is_active:
        raise error
    return user
