from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models
from .. import utils, oauth2


# login HR
router = APIRouter(prefix="/login",
                   tags=["login"])


@router.post("/hr")
def login(user_creditials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.HR).filter(
        models.HR.email == user_creditials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    respond = utils.verify(user_creditials.password, user.password)

    if not respond:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    key = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token":  key,
            "token_type": "bearer"}
