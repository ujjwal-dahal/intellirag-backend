import re
from datetime import date, time

from pydantic import BaseModel, Field, field_validator


class BookingDetails(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: str = Field(max_length=255)
    interview_date: date
    interview_time: time

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Name must contain at least 2 characters.")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip()

        email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(email_pattern, value):
            raise ValueError("Invalid email address.")

        return value

    @field_validator("interview_date")
    @classmethod
    def validate_interview_date(cls, value: date) -> date:
        if value <= date.today():
            raise ValueError("Interview date must be in the future.")

        return value

    @field_validator("interview_time")
    @classmethod
    def validate_interview_time(cls, value: time) -> time:
        return value
