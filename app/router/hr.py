from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schema
from ..utils import generate_password
from .. import models


router = APIRouter(prefix="/hr", tags=["HR"])


@router.post("/", tags=["HR"], response_model=schema.HRResponse)
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
