import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = os.getenv("DATABASE_HOST", "localhost")
user = os.getenv("DATABASE_USER", "root")
password = os.getenv("DATABASE_PASSWORD", "rootpassword")
database = os.getenv("DATABASE_DATABASE", "google_play_store")
port = os.getenv("DATABASE_PORT", "3306")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
# engine = create_engine("mysql+pymysql://root:MySql!Luke1@localhost:3306/google_play_store")

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
