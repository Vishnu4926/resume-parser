import json
import time

from database.connection import SessionLocal
from database.models import Resume

from services.embedding_service import (
    create_embedding,
    resume_to_text
)

db = SessionLocal()

resumes = db.query(Resume).all()

for resume in resumes:

    if resume.embedding:
        continue

    try:

        print(
            f"Creating embedding for {resume.id} - {resume.full_name}"
        )

        data = {
            "full_name": resume.full_name,
            "skills": resume.skills or [],
            "education": resume.education or [],
            "experience": resume.experience or []
        }

        text = resume_to_text(data)

        embedding = create_embedding(text)

        resume.embedding = json.dumps(
            embedding
        )

        db.commit()

        print(
            f"Saved embedding for {resume.id}"
        )

        time.sleep(3)

    except Exception as e:

        print(
            f"Failed on {resume.id}: {e}"
        )

        db.rollback()

db.close()

print("Done")
