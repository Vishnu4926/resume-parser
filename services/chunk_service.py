import json

from services.embedding_service import (
    create_embedding
)

from database.chunk_crud import (
    create_chunk
)


def create_resume_chunks(
    db,
    resume
):

    chunks = []

    if resume.skills:

        chunks.append(
            f"Skills: {resume.skills}"
        )

    if resume.education:

        chunks.append(
            f"Education: {resume.education}"
        )

    if resume.experience:

        chunks.append(
            f"Experience: {resume.experience}"
        )

    for chunk_text in chunks:

        embedding = create_embedding(
            chunk_text
        )

        create_chunk(
            db=db,
            resume_id=resume.id,
            chunk_text=chunk_text,
            embedding=json.dumps(
                embedding
            )
        )
