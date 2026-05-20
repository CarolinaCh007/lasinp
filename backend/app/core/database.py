from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine

# 🔹 Leer credenciales directamente de variables de entorno (bypass Pydantic para BD)
import os
DB_USER = os.getenv("DB_USER", "lasin_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lasin_user")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "lasin_db")

# Construir URL manualmente con encoding explícito
from urllib.parse import quote_plus
pwd_encoded = quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql://{DB_USER}:{pwd_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔧 [DATABASE.PY] Conectando a: {DB_HOST}:{DB_PORT}/{DB_NAME} como {DB_USER}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    client_encoding="utf8",
    connect_args={"options": "-c client_encoding=utf8"}
)

@event.listens_for(Engine, "connect")
def set_default_encoding(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    try:
        cursor.execute("SET client_encoding TO 'UTF8'")
    finally:
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()