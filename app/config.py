import os

class Config:
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    PROCESSED_DIR = os.getenv("PROCESSED_DIR", "processed")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max upload
    ALLOWED_EXTENSIONS = {"pdf"}