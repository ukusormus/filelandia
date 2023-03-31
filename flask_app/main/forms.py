import os.path

from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from ..models import File
from flask_app.extensions import db


class FileUploadForm(FlaskForm):
    file = FileField(validators=[
        FileRequired(message="File cannot be empty.")
    ])

    def validate(self, extra_validators=None):
        """Validate the form."""
        initial_validation = super(FileUploadForm, self).validate()
        if not initial_validation:
            return False

        # Sanitize filename
        filename = secure_filename(self.file.data.filename)
        if filename == "":
            self.form_errors.append("Filename must not be empty and cannot contain illegal characters.")
            return False
        if len(filename) > 255:
            self.form_errors.append("Filename too long.")
            return False

        # see config.py for MAX_CONTENT_LENGTH, meaning max upload size that Flask will accept

        # Checks passed
        # // move this whole logic to models.py?
        path = current_user.get_uploaded_files_dir()
        path.mkdir(mode=0o600, parents=True, exist_ok=True)
        file_path = os.path.join(path, filename)

        # Behavior right now is to overwrite file if it existed with the same name
        exists = False
        if os.path.exists(file_path):
            exists = True

        # - Save file to filesystem
        self.file.data.save(file_path)

        # - Save file's metadata to database
        if exists:
            db.session.query(File).filter_by(filename=filename).delete()
            flash("Overwrote file with the same name.")
        metadata = File(
            filename=filename, file_size=os.path.getsize(file_path),
            mimetype=self.file.data.mimetype, user_id=current_user.id
        )
        db.session.add(metadata)
        db.session.commit()

        return True
