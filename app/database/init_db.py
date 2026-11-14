# project imports
from app.database.base import Base
from app.database.connection import engine

"""Import models so SQLAlchemy can register their tables"""
from app.database.models import Document, InterviewBooking


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully...")


if __name__ == "__main__":
    create_tables()
