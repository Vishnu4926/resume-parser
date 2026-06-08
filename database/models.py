from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    Text
)

from database.connection import Base


class Resume(Base):

    __tablename__ = "resumes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(String)

    email = Column(String)

    phone = Column(String)

    skills = Column(JSON)

    education = Column(JSON)

    experience = Column(JSON)

    file_url = Column(String)

    embedding = Column(
        Text,
        nullable=True
    )


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True
    )

    email = Column(
        String,
        unique=True
    )

    password = Column(String)
