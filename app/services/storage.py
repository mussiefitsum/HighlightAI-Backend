import os
import uuid
from flask import current_app

def allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def ensure_dirs():
    os.makedirs(current_app.config["UPLOAD_DIR"], exist_ok=True)
    os.makedirs(current_app.config["PROCESSED_DIR"], exist_ok=True)

def save_upload(file_storage):
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    new_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_DIR"], new_name)
    file_storage.save(save_path)
    return new_name, save_path
