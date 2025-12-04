# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from domain.question import question_router
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(question_router.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def read_root():
    return {'message': 'Hello World'}