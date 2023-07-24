from pydantic import BaseModel
from typing import Optional


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
    name: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class InterviewStart(BaseModel):
    title: str


class InterviewResponse(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


class Interview_code(BaseModel):
    code: str


class Answer(BaseModel):
    answer: str
