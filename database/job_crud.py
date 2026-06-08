from models.job_posting import JobPosting


def create_job(
    db,
    title,
    description,
    embedding
):

    job = JobPosting(
        title=title,
        description=description,
        embedding=embedding
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    return job


def get_job(db, job_id):

    job = db.query(JobPosting).filter(
        JobPosting.id == job_id
    ).first()

    if not job:
        return None

    return {
        "id": job.id,
        "title": job.title,
        "description": job.description
    }

def get_jobs(db):

    jobs = db.query(JobPosting).all()

    return [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description
        }
        for job in jobs
    ]
