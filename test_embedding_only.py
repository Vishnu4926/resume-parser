from services.embedding_service import create_embedding

embedding = create_embedding(
    "Python FastAPI PostgreSQL"
)

print(len(embedding))
