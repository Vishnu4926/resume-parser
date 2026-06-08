from pydantic import BaseModel


class EvaluationItem(BaseModel):
    question: str
    expected_answer: str
