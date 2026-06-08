from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

from database.connection import Base


class ResumeChunk(Base):

    __tablename__ = "resume_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id")
    )

    chunk_text = Column(
        Text
    )

    embedding = Column(
        Text
    )
