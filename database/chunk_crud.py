from models.resume_chunk import (
    ResumeChunk
)


def create_chunk(
    db,
    resume_id,
    chunk_text,
    embedding
):

    chunk = ResumeChunk(
        resume_id=resume_id,
        chunk_text=chunk_text,
        embedding=embedding
    )

    db.add(chunk)

    db.commit()

    db.refresh(chunk)

    return chunk


def get_chunks(
    db
):

    return (
        db.query(
            ResumeChunk
        )
        .all()
    )
