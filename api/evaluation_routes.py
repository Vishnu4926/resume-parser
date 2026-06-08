from services.evaluation_service import (
    evaluate_rag,
    evaluate_rag_batch
)

from typing import List

from schemas.batch_evaluation_schema import (
    EvaluationItem
)

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from auth.dependencies import (
    get_current_user
)

from database.connection import (
    SessionLocal
)

from schemas.evaluation_schema import (
    EvaluationRequest
)

from services.evaluation_service import (
    evaluate_rag
)

router = APIRouter()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/evaluate-rag")
def evaluate_endpoint(
    request: EvaluationRequest,
    current_user: str = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    return evaluate_rag(
        request.question,
        request.expected_answer,
        db
    )

@router.post(
    "/evaluate-rag-batch"
)
def evaluate_batch_endpoint(

    requests: List[
        EvaluationItem
    ],

    current_user: str = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    return evaluate_rag_batch(
        requests,
        db
    )
