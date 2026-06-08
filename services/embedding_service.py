from utils.metrics import Timer
from utils.logger import logger

import vertexai

from vertexai.language_models import (
    TextEmbeddingModel
)

PROJECT_ID = "vertex-ai-learning-497706"
LOCATION = "us-central1"


def create_embedding(text: str):

    logger.info(
        "Creating embedding"
    )

    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION
    )

    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-005"
    )

    with Timer() as timer:

        embedding = model.get_embeddings(
            [text]
        )[0]

    logger.info(
        f"Embedding time: {timer.elapsed:.2f}s"
    )

    logger.info(
        "Embedding created"
    )

    return embedding.values


def resume_to_text(data):

    parts = []

    parts.append(
        data.get("full_name", "")
    )

    parts.extend(
        data.get("skills", [])
    )

    for edu in data.get(
        "education",
        []
    ):
        parts.append(
            str(edu)
        )

    for exp in data.get(
        "experience",
        []
    ):
        parts.append(
            str(exp)
        )

    return " ".join(parts)
