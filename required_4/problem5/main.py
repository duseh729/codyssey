# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


@app.post('/question')
def create_question(subject: str, content: str, db: Session = Depends(get_db)):
    question = models.Question(
        subject=subject,
        content=content
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question
