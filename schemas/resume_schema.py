from pydantic import BaseModel
from typing import List


class ResumeResponse(BaseModel):
    full_name: str
    email: str
    phone: str
    skills: List[str]
