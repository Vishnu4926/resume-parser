import json
from models.job import Job


def create_job(db, filename: str):
    job = Job(filename=filename, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def mark_processing(db, job_id: int, file_url: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    job.status = "processing"
    job.file_url = file_url
    db.commit()


def mark_done(db, job_id: int, result: dict):
    job = db.query(Job).filter(Job.id == job_id).first()
    job.status = "done"
    job.result = json.dumps(result)
    db.commit()


def mark_failed(db, job_id: int, error: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    job.status = "failed"
    job.error = error
    db.commit()
