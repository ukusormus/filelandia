import os
from pathlib import Path


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_ECHO = True

    # Uploads config
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"  # for Files' metadata & Users (see models.py); ./instance/db.sqlite
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB (max upload file size). Enforced by Flask
    USER_UPLOADS_BASE_FOLDER = os.path.join(Path(__file__).parent.resolve(), "instance/", "user_uploads")


    # MAX_FILENAME_LENGTH = 128
    #
    # # Username/password config
    # MIN_USERNAME_LENGTH = 3
    # MAX_USERNAME_LENGTH = 32
    # MIN_PASSWORD_LENGTH = 8
    # MAX_PASSWORD_LENGTH = 128
