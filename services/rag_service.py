import json

from utils.logger import logger
from utils.metrics import Timer

from database.chunk_crud import (
    get_chunks
)

from database.crud import (
    get_resume_by_id
)

from services.embedding_service import (
    create_embedding
)

from services.gemini_service import (
    model
)

from utils.vector_utils import (
    cosine_similarity
)


def recruiter_chat(
    question,
    db
):

    logger.info(
        f"Recruiter question: {question}"
    )

    query_embedding = create_embedding(
        question
    )

    chunks = get_chunks(db)

    matches = []

    for chunk in chunks:

        if not chunk.embedding:
            continue

        chunk_embedding = json.loads(
            chunk.embedding
        )

        score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        matches.append(
            (
                score,
                chunk
            )
        )

    matches.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    top_chunks = matches[:10]

    candidate_context = {}

    for score, chunk in top_chunks:

        resume = get_resume_by_id(
            db,
            chunk.resume_id
        )

        if not resume:
            continue

        if resume.id not in candidate_context:

            candidate_context[
                resume.id
            ] = {
                "name": resume.full_name,
                "chunks": []
            }

        candidate_context[
            resume.id
        ]["chunks"].append(
            chunk.chunk_text
        )

    context = ""

    for candidate in candidate_context.values():

        context += f"""
Candidate:
Name: {candidate['name']}

Information:
{' '.join(candidate['chunks'])}

"""

    prompt = f"""
You are an expert recruiter.

Use ONLY the candidate information below.

If the answer is not present in the data,
respond exactly with:

"I could not find enough information."

Question:
{question}

Candidates:
{context}
"""

    with Timer() as timer:

        response = model.generate_content(
            prompt
        )

    logger.info(
        f"RAG generation time: {timer.elapsed:.2f}s"
    )

    logger.info(
        "RAG answer generated"
    )

    return {
        "answer": response.text
    }
