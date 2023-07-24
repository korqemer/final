from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema
from ..utils import generate_password
from .. import models
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils, oauth2app


router = APIRouter(
    prefix="/applicant", tags=["APPLICANTS"]
    )


# applicant registration +
@router.post("/register", status_code=status.HTTP_201_CREATED,
             response_model=schema.ApplicantResponse)
def register(applicant: schema.Applicant,
             db: Session = Depends(get_db)):
    user = db.query(models.Applicant).filter(
        models.Applicant.email == applicant.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail="ALREADY EXISTS")
    hashed_password = generate_password(applicant.password)
    applicant.password = hashed_password
    new_user = models.Applicant(**applicant.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Applicant Login +
@router.post("/login")
def login(user_creditials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.HR).filter(
        models.Applicant.email == user_creditials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    respond = utils.verify(user_creditials.password, user.password)

    if not respond:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    key = oauth2app.create_access_token(data={"user_id": user.id})

    return {"access_token":  key,
            "token_type": "bearer"}


# change the interview information +
@router.patch("/interview/{interview_id}")
def update_interview(interview_id: str, db: Session = Depends(get_db),
                     current_app: int = Depends(oauth2app.get_current_user)):
    interview = db.query(models.Interview).filter(
        models.Interview.id_code == interview_id).first()
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details="NO Interview")
    interview.user_id = current_app.id
    db.commit()
    db.refresh(interview)
    return interview
