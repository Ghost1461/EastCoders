from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import time

from app.core.config import DATABASE_URL


MAX_RETRIES = 10
RETRY_DELAY = 3


engine = None

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()

        print("Database connected successfully.")
        break

    except OperationalError:
        print(f"Database not ready... retrying ({attempt + 1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)

if engine is None:
    raise Exception("Could not connect to database.")


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()