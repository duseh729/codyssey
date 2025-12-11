# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import contextlib

SQLITE_URL = 'sqlite:///./app.db'

# engine = 실제 db와 연결하는 핵심 객체
engine = create_engine(
    SQLITE_URL,
    # SQLite의 경우, check_same_thread 옵션을 False로 설정해야 여러 스레드에서 접근 가능
    connect_args={'check_same_thread': False}
)

# Session() 객체를 만들어주는 함수
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
