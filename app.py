from models.job_posting import JobPosting

from api.job_routes import (
    router as job_router
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.resume_routes import router
from auth.auth_routes import router as auth_router

from database.connection import (
    Base,
    engine
)

# Import ALL models before create_all()

from database.models import (
    Resume,
    User
)

from models.job import Job

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resume Parser API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)
app.include_router(auth_router)



app.include_router(
    job_router
)
