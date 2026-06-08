from utils.matching import calculate_match_score

import json
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Query,
    Depends,
    BackgroundTasks,
    HTTPException
)
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from database.connection import SessionLocal
from database.crud import (
    search_by_skill,
    create_resume,
    get_resumes,
    get_resume_by_id,
    search_by_name
)
from models.job import Job
from services.embedding_service import create_embedding
from services.gemini_service import parse_resume
from services.job_service import create_job
from services.resume_worker import process_resume_job
from services.storage_service import (
    upload_resume,
    generate_signed_url
)
from utils.vector_utils import cosine_similarity

router = APIRouter()

# Dependency to get DB session (Day 8 best practice)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search")
def search_resumes(
    name: str = Query(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        results = search_by_name(
            db,
            name
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/resumes/{resume_id}")
def get_resume(
    resume_id: int, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = get_resume_by_id(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get("/resumes")
def get_all_resumes(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_resumes(db)

@router.post("/parse-resume")
async def parse_resume_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        file_bytes = await file.read()
        
        # 1. Try uploading to storage
        try:
            file_url = upload_resume(file_bytes, file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Storage upload failed: {str(e)}")
            
        # 2. Try parsing with Vertex AI
        try:
            result = parse_resume(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Vertex AI Parsing failed: {str(e)}")

        # 3. Try saving to Database
        if result.get("status") == "success":

            db = SessionLocal()

            try:

                resume_text = f"""
                Name: {result['data'].get('full_name', '')}

                Skills: {result['data'].get('skills', [])}

                Education: {result['data'].get('education', [])}

                Experience: {result['data'].get('experience', [])}
                """

                embedding = create_embedding(
                    resume_text
                )

                saved_resume = create_resume(
                    db,
                    result["data"],
                    file_url,
                    json.dumps(embedding)
                )

                result["database_id"] = saved_resume.id

            except Exception as e:

                raise HTTPException(
                    status_code=500,
                    detail=f"Database save failed: {str(e)}"
                )

            finally:

                db.close()

        else:

            raise HTTPException(
                status_code=400,
                detail=f"Parsing status returned failure: {result}"
            )



        result["file_url"] = file_url
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        # Catch-all for any other unexpected error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@router.get("/search/skill")
def search_skill(
    skill: str,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        results = search_by_skill(
            db,
            skill
        )

        return results

    finally:
        db.close()

@router.post("/match-job/{resume_id}")
def match_job(
    resume_id: int,
    job_description: str,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        resume = get_resume_by_id(
            db,
            resume_id
        )

        if not resume:

            return {
                "error": "Resume not found"
            }

        if not resume.embedding:

            return {
                "error": "Resume has no embedding"
            }

        job_embedding = create_embedding(
            job_description
        )

        resume_embedding = json.loads(
            resume.embedding
        )

        score = calculate_match_score(
            job_embedding,
            resume_embedding
        )

        return {
            "resume_id": resume.id,
            "candidate_name": resume.full_name,
            "match_score": round(
                score * 100,
                2
            )
        }

    finally:
        db.close()



@router.get("/resume-download/{resume_id}")
def download_resume(
    resume_id: int,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        resume = get_resume_by_id(
            db,
            resume_id
        )

        if not resume:

            return {
                "message": "Resume not found"
            }

        filename = (
            resume.file_url
            .split("/")[-1]
        )

        signed_url = generate_signed_url(
            filename
        )

        return {
            "download_url": signed_url
        }

    finally:
        db.close()


@router.post("/upload-resume")
async def upload_resume_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):

    file_bytes = await file.read()

    db = SessionLocal()

    try:

        job = create_job(
            db,
            file.filename
        )

        background_tasks.add_task(
            process_resume_job,
            job.id,
            file_bytes,
            file.filename
        )

        return {
            "job_id": job.id,
            "status": "queued"
        }

    finally:
        db.close()



@router.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:

            return {
                "error": "Job not found"
            }

        result = None

        if job.result:
            result = json.loads(
                job.result
            )

        return {
            "job_id": job.id,
            "status": job.status,
            "result": result,
            "error": job.error,
            "file_url": job.file_url
        }

    finally:
        db.close()

@router.get("/semantic-search")
def semantic_search(
    query: str,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        query_embedding = create_embedding(
            query
        )

        resumes = get_resumes(db)

        results = []

        for resume in resumes:

            if not resume.embedding:
                continue

            resume_embedding = json.loads(
                resume.embedding
            )

            score = cosine_similarity(
                query_embedding,
                resume_embedding
            )

            results.append(
                {
                    "resume_id": resume.id,
                    "name": resume.full_name,
                    "score": score
                }
            )

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:5]

    finally:
        db.close()

@router.post("/match-all")
def match_all_resumes(
    job_description: str,
    current_user: str = Depends(get_current_user)
):

    db = SessionLocal()

    try:

        job_embedding = create_embedding(
            job_description
        )

        resumes = get_resumes(
            db
        )

        matches = []

        for resume in resumes:

            if not resume.embedding:
                continue

            resume_embedding = json.loads(
                resume.embedding
            )

            score = cosine_similarity(
                job_embedding,
                resume_embedding
            )

            matches.append(
                {
                    "resume_id": resume.id,
                    "name": resume.full_name,
                    "score": round(
                        score * 100,
                        2
                    )
                }
            )

        matches.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return matches[:10]

    finally:
        db.close()
