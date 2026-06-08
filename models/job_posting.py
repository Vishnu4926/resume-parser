from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from database.connection import Base


class JobPosting(Base):

    __tablename__ = "job_postings"

    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(String)

    description = Column(Text)

    embedding = Column(Text)
