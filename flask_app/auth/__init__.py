"""User authentication module."""
min_username_length = 3
max_username_length = 32
min_password_length = 3  # ! dev / debug
max_password_length = 256

max_filename_length = 128

from flask_app.auth import views
