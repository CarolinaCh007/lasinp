from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
import os

class Settings(BaseSettings):
    # 🔹 Aplicación
    APP_NAME: str = "Sistema Educativo API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # 🔹 JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_change_me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 🔹 Base de datos (SOLO credenciales separadas, SIN DATABASE_URL como campo)
    DB_USER: str = os.getenv("DB_USER", "lasin_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "lasin_user")  # ← Cambiar "lasin123" → "lasin_user"
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "lasin_db")

    @property
    def DATABASE_URL(self) -> str:
        """Construye la URL con encoding UTF-8 seguro para contraseñas"""
        pwd_encoded = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{pwd_encoded}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # 🔹 Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }

# Singleton cacheado
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# 🔍 DEBUG: Imprimir URL generada al cargar (solo desarrollo)
if settings.ENVIRONMENT == "development":
    print(f"🔧 [CONFIG] DATABASE_URL generada: {settings.DATABASE_URL}")