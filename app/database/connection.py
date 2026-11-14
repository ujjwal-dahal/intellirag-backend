from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# project import
from app.core.config import settings

"""Database Connection"""
engine = create_engine(
    url=settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
)


"""Session is used to Manage Database Operations"""
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


"""Providing Single Session on Each Request"""


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
