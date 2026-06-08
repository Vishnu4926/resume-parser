from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text
)

from datetime import datetime

from database.connection import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    status = Column(
        String,
        default="pending"
    )

    file_url = Column(
        Text,
        nullable=True
    )

    filename = Column(
        String,
        nullable=True
    )

    result = Column(
        Text,
        nullable=True
    )

    error = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
