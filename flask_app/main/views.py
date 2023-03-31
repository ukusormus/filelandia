import os

from flask import Blueprint, render_template, flash, url_for, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from flask_app.main.forms import FileUploadForm
from ..extensions import db
from ..models import File

main = Blueprint("main", __name__, static_folder="../static", url_prefix="/files")


@main.route("/get_files")
@login_required
def get_files_metadata_json():
    """Get current user's files list as JSON."""
    return jsonify([
        {
            "filename": file.filename,
            "uploadDate": file.upload_date.isoformat(),
            "fileSize": file.file_size,
            "mimeType": file.mimetype
        }
        for file in current_user.files
    ])


@main.route("/view")
@login_required
def view():
    return render_template("files/list.html")


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = FileUploadForm()

    if form.validate_on_submit():
        # Checks passed (POST request; see main/forms.py#validate() for other checks)

        flash("File upload successful!")
        return redirect(url_for(".upload"))

    return render_template("files/upload.html", form=form)


@main.route("/delete/<filename>", methods=["DELETE"])
@login_required
def delete(filename):
    # // move this to models.py?
    file = db.session.query(File).filter_by(filename=filename, user_id=current_user.id).first()

    if file is None:
        flash("Invalid file deletion request.")
        return {}, 418  # I'm a Teapot :0

    os.remove(os.path.join(current_user.get_uploaded_files_dir(), file.filename))
    db.session.delete(file)
    db.session.commit()

    flash("File deleted successfully!")
    return {}, 200


@main.route("/download/<filename>")
@login_required
def download(filename):
    return send_from_directory(
        directory=current_user.get_uploaded_files_dir(),
        path=filename,
        as_attachment=True
    )


@main.errorhandler(413)
def request_entity_too_large(error):
    flash(f"File too large. Max size: {current_app.config['MAX_CONTENT_LENGTH'] / (1 << 20)} MB.")
    return redirect(url_for(".upload"))
