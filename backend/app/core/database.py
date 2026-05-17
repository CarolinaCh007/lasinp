from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Pool de conexiones + ping automático para mantener viva la conexión Docker
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependencia para inyectar sesión en los endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()