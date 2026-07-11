import os
import secrets

from dotenv import load_dotenv


load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if APP_ENV == "production" and not SECRET_KEY:
    raise RuntimeError("SECRET_KEY must be configured in production")
if APP_ENV == "production" and not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be configured in production")


class Config:
    SECRET_KEY = SECRET_KEY or secrets.token_urlsafe(48)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///course_design-dev.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    TOKEN_MAX_AGE = int(os.getenv("TOKEN_MAX_AGE", "43200"))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173")
    LOGIN_RATE_WINDOW_SECONDS = int(os.getenv("LOGIN_RATE_WINDOW_SECONDS", "900"))
    LOGIN_RATE_MAX_ATTEMPTS = int(os.getenv("LOGIN_RATE_MAX_ATTEMPTS", "8"))
