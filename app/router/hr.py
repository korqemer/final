from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema
from ..utils import generate_password
from .. import models
import random
import string
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils, oauth2


router = APIRouter(prefix="/hr", tags=["HR"])


# HR registration
@router.post("/register", response_model=schema.HRResponse)
def register(new_hr: schema.HR,
             db: Session = Depends(get_db)):
    user = db.query(models.HR).filter(models.HR.email == new_hr.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="ALREADY EXISTS")
    hashed_password = generate_password(new_hr.password)
    new_hr.password = hashed_password
    new_user = models.HR(email=new_hr.email, password=new_hr.password,
                         name=new_hr.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


# owner_id с JWT
# чекнуть чтобы не было похожий code в БД
@router.post("/interview")
def create_interview(new_interview: schema.InterviewStart,
                     db: Session = Depends(get_db),
                     current_hr: int = Depends(oauth2.get_current_user)):
    code = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    hr = int(current_hr.id)
    code = str(hr) + code
    interview = models.Interview(
        title=new_interview.title,
        owner_id=hr,
        id_code=code
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


# get all interviews created by this person
@router.get("/interview")
def get_interviews(db: Session = Depends(get_db),
                   current_hr: int = Depends(oauth2.get_current_user)):
    hr = current_hr.id
    interviews = db.query(models.Interview).filter(
        models.Interview.owner_id == hr).all()
    return interviews


# HR LOGIN
@router.post("/login")
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
