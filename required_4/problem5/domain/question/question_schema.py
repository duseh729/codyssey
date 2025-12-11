# domain/question/question_schema.py
import datetime
from pydantic import BaseModel, validator

# 질문 목록/상세
class _Question(BaseModel):
    id: int
    subject: str | None = None
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

# 질문 생성
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v