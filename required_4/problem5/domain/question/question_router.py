# domain/question/question_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Question
from typing import List
from .question_schema import _Question, QuestionCreate

router = APIRouter(
    prefix="/api/question",
    tags=["question"]
)

# 1) 질문 목록 조회
@router.get("/list", response_model=List[_Question])
def question_list(db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return questions

# 2) 질문 생성
@router.post("/create")
def question_create(payload: QuestionCreate, db: Session = Depends(get_db)):
    question = Question(
        subject=payload.subject,
        content=payload.content,
    )

    db.add(question)
    db.commit()
    db.refresh(question)
    return question
