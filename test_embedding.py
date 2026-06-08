from services.embedding_service import (
    create_embedding
)

embedding = create_embedding(
    "Python FastAPI Developer"
)

print(type(embedding))
print(len(embedding))
print(embedding[:5])
