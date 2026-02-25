"""
Migration script to create all tables in PostgreSQL using SQLAlchemy models.
Run this once after updating models.py.
"""
from sqlalchemy import create_engine
from models import Base
import os

def get_db_url():
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return "postgresql://postgres:Facebooklit@localhost:5432/manidhar_ai"

if __name__ == "__main__":
    engine = create_engine(get_db_url())
    Base.metadata.create_all(engine)
    print("All tables created.")