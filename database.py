import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config import get_settings



SQLALCHEMY_DATABASE_URL = get_settings().database_url


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
