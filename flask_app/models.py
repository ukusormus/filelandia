import os
from pathlib import Path

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .auth import max_username_length, max_filename_length
from .extensions import db, login_manager


@login_manager.user_loader
def load_user(id: str):
    return db.session.query(User).get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    username = db.Column(db.String(max_username_length), index=True, unique=True)
    password_hash = db.Column(db.Text())

    # Each user can have multiple files related to them
    files = db.relationship("File", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_uploaded_files_dir(self):
        return Path(os.path.join(
            current_app.config["USER_UPLOADS_BASE_FOLDER"], str(self.id)
        ))


class File(db.Model):
    id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    filename = db.Column(db.String(max_filename_length))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_size = db.Column(db.Integer)
    mimetype = db.Column(db.String(255))

    # Each file is owned by a user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="files")
