from database.models import Resume


def get_resumes(db):

    return db.query(Resume).all()


def get_resume_by_id(
    db,
    resume_id
):

    return (
        db.query(Resume)
        .filter(
            Resume.id == resume_id
        )
        .first()
    )


def search_by_name(
    db,
    name
):

    return (
        db.query(Resume)
        .filter(
            Resume.full_name.ilike(
                f"%{name}%"
            )
        )
        .all()
    )


def search_by_skill(
    db,
    skill
):

    resumes = db.query(
        Resume
    ).all()

    results = []

    for resume in resumes:

        skills = resume.skills or []

        for s in skills:

            if skill.lower() in s.lower():

                results.append(
                    resume
                )

                break

    return results


def create_resume(
    db,
    data,
    file_url,
    embedding=None
):

    resume = Resume(

        full_name=data.get("full_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        skills=data.get("skills"),
        education=data.get("education"),
        experience=data.get("experience"),
        file_url=file_url,
        embedding=embedding
    )

    db.add(resume)

    db.commit()

    db.refresh(resume)

    return resume
