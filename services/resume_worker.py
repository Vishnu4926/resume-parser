import json

from database.connection import SessionLocal
from database.crud import create_resume

from services.storage_service import upload_resume
from services.gemini_service import parse_resume

from services.embedding_service import (
    create_embedding,
    resume_to_text
)

from services.job_service import (
    mark_processing,
    mark_done,
    mark_failed
)


def process_resume_job(
    job_id: int,
    file_bytes: bytes,
    filename: str
):

    db = SessionLocal()

    try:

        # Upload PDF
        file_url = upload_resume(
            file_bytes,
            filename
        )

        mark_processing(
            db,
            job_id,
            file_url
        )

        # Parse resume
        result = parse_resume(
            file_bytes
        )

        if result.get("status") != "success":

            mark_failed(
                db,
                job_id,
                str(result)
            )

            return

        # Save resume
        saved_resume = create_resume(
            db,
            result["data"],
            file_url
        )

        # Create embedding
        resume_text = resume_to_text(
            result["data"]
        )

        print("Creating embedding...")

        embedding = create_embedding(
            resume_text
        )

        print(
            "Embedding length:",
            len(embedding)
        )

        # Save embedding
        saved_resume.embedding = json.dumps(
            embedding
        )

        print(
            "Saving embedding to database..."
        )

        db.commit()

        print(
            "Embedding saved."
        )

        result["database_id"] = (
            saved_resume.id
        )

        mark_done(
            db,
            job_id,
            result
        )

    except Exception as e:

        print(
            "WORKER ERROR:",
            str(e)
        )

        mark_failed(
            db,
            job_id,
            str(e)
        )

    finally:
        db.close()
