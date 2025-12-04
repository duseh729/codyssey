# domain/question/question_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Question

router = APIRouter(
    prefix="/api/question",
    tags=["question"]
)

# 1) 질문 목록 조회
@router.get("/list")
def question_list(db: Session = Depends(get_db)):
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return {
        "count": len(questions),
        "items": questions
    }

# 2) 질문 생성
@router.post("/create")
def create_question(payload: dict, db: Session = Depends(get_db)):
    """
    입력 예시(JSON):
    {
        "subject": "제목",
        "content": "내용"
    }
    """
    # payload: {"subject": "...", "content": "..."}

    question = Question(
        subject=payload.get("subject"),
        content=payload.get("content"),
    )

    db.add(question)
    db.commit()
    db.refresh(question)
    return question
