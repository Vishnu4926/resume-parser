import vertexai

from vertexai.language_models import (
    TextEmbeddingModel
)

PROJECT_ID = "vertex-ai-learning-497706"
LOCATION = "us-central1"


def create_embedding(text: str):

    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION
    )

    model = TextEmbeddingModel.from_pretrained(
        "text-embedding-005"
    )

    embedding = model.get_embeddings(
        [text]
    )[0]

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
