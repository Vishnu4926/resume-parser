import json

from utils.vector_utils import cosine_similarity


def calculate_match_score(
    job_embedding,
    resume_embedding
):

    return cosine_similarity(
        job_embedding,
        resume_embedding
    )
