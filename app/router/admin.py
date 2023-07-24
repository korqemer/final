from fastapi import APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema
from .. import models
from typing import List


router = APIRouter(
    prefix="/admin", tags=["ADMIN"]
    )


# Get all applicants
@router.get("/applicants", response_model=List[schema.ApplicantResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Applicant).all()
    return users


@router.get("/applicants/{id}", response_model=schema.ApplicantResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Applicant).filter(models.Applicant.id == id).first()
    return user


# problem with SCHEMA
@router.get("/hr", response_model=List[schema.HRResponse])
def get_hrs(db: Session = Depends(get_db)):
    hrs = db.query(models.HR).all()
    return hrs


@router.get("/hr/{id}", response_model=schema.HRResponse)
def get_hr(id: int, db: Session = Depends(get_db)):
    hr = db.query(models.HR).filter(models.HR.id == id).first()
    return hr


@router.get("/interview")
def get_all_interview(db: Session = Depends(get_db)):
    return db.query(models.Interview).all()
