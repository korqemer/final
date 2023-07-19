from fastapi import APIRouter, Depends
from ..database import get_db
from ..gpt import get_question, get_score
from sqlalchemy.orm import Session
from .. import schema
from .. import models

router = APIRouter(tags=["interview"], prefix="/interview")


@router.get("/question")
async def question(db: Session = Depends(get_db)):
    new_question = models.Question()
    return {"question": get_question()}


@router.post("/question")
async def answer(answer: schema.Answer, db: Session = Depends(get_db)):
    new_answer = models.Question(question = answer.question, answer = answer.answer,
                                 interview_id = 1)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer
