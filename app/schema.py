from pydantic import BaseModel
from typing import Optional


class Answer(BaseModel):
    question: str
    answer: str


class Applicant(BaseModel):
    name: str
    surname: str
    password: str
    email: str


class ApplicantResponse(BaseModel):
    name: str
    surname: str
    email: str


class HR(BaseModel):
    name: str
    email: str
    password: str


class HRResponse(BaseModel):
    email: str
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None