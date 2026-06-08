from pydantic import BaseModel


class EvaluationRequest(BaseModel):

    question: str

    expected_answer: str
