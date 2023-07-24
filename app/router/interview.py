from fastapi import APIRouter, Depends
from ..database import get_db
from ..gpt import get_question, get_score
from sqlalchemy.orm import Session
from .. import schema
from .. import models


router = APIRouter(
    tags=["interview"],
    prefix="/interview")


# we create the question instance here
@router.get("/{interview_code}")
def question(interview_code: str, db: Session = Depends(get_db)):
    interview = db.query(models.Interview).filter(
        models.Interview.id_code == interview_code).first()
    new_question = models.Question(
        question=get_question(),
        interview_id=interview.id
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


# we take question instance and put the value
@router.post("/{interview_code}/{question_id}")
def answer(answer: schema.Answer,
           question_id: int, interview_code: str,
           db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(
        models.Question.id == question_id).first()
    question.answer = answer.answer
    question.score = get_score(question.question, question.answer)
    db.commit()
    db.refresh(question)
    edited_question = db.query(models.Question).filter(
        models.Question.id == question_id).first()
    return edited_question
