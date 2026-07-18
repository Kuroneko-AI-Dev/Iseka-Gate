import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event

load_dotenv()

DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(
    DATABASE_URL + "?sslmode=require",
    echo=os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"
)


@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET search_path TO public")
    cursor.close()

    
from sqlalchemy import text

with engine.connect() as conn:
    print("DB:", conn.execute(text("SELECT current_database()")).fetchone())
    print("USER:", conn.execute(text("SELECT current_user")).fetchone())
    print("SEARCH:", conn.execute(text("SHOW search_path")).fetchone())
    print(
        "USERS:",
        conn.execute(text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name='users'
        """)).fetchall()
    )
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

