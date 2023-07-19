from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


class HR(Base):
    __tablename__ = "hrs"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Interview(Base):
    __tablename__ = "interviews"
    title = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text("now()"))
    owner_id = Column(Integer,
                      ForeignKey("hrs.id", ondelete="CASCADE"),
                      nullable=False)
    user_id = Column(Integer,
                     ForeignKey("applicants.id", ondelete="CASCADE"),
                     nullable=False)
    finished = Column(Boolean, nullable=False)
    score = Column(Float)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    interview_id = Column(Integer,
                          ForeignKey("interviews.id", ondelete="CASCADE"),
                          nullable=False)
    answered_at = Column(TIMESTAMP(timezone=True), nullable=False,
                         server_default=text("now()"))
    score = Column(Integer, nullable=False)
