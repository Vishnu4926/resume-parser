import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from auth.dependencies import get_current_user

from database.connection import SessionLocal

from database.job_crud import (
    create_job,
    get_jobs,
    get_job
)

from services.embedding_service import (
    create_embedding
)

from services.rag_service import (
   recruiter_chat
)

from schemas.chat_schema import ChatRequest



router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/job-postings")
def create_new_job(
    title: str,
    description: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    embedding = create_embedding(
        description
    )

    job = create_job(
        db,
        title,
        description,
        json.dumps(embedding)
    )

    return {
        "job_id": job.id,
        "title": job.title
    }


@router.get("/job-postings")
def list_jobs(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return get_jobs(db)


@router.get("/job-postings/{job_id}")
def get_single_job(
    job_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    job = get_job(
        db,
        job_id
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@router.post("/recruiter-chat")
def chat_with_candidates(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return recruiter_chat(
        request.question,
        db
    )
