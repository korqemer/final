from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema
from ..utils import generate_password
from .. import models
from typing import List
from .. import oauth2


router = APIRouter(
    prefix="/applicant", tags=["APPLICANTS"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED,
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


# add ApplicatnRespnse
@router.get("/", response_model=List[schema.ApplicantResponse])
def get_users(db: Session = Depends(get_db),
              current_hr: int = Depends(oauth2.get_current_user)
              ):
    applicants = db.query(models.Applicant).all()
    return applicants


@router.get("/{id}", response_model=schema.ApplicantResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Applicant).filter(models.Applicant.id == id).first()
    return user
