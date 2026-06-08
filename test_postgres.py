# test_postgres.py

from sqlalchemy import create_engine

DATABASE_URL =  "postgresql://resume_user:Vishnu%404926""@35.254.159.162:5432/resume_parser"

engine = create_engine(DATABASE_URL)

connection = engine.connect()

print(connection)

connection.close()
