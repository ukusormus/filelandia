from flask import Flask
from config import Config


def create_app(config_object=Config):
    # Initialize Flask app with given configuration
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Register extensions and blueprints
    register_blueprints(app)
    register_extensions(app)

    return app


def register_extensions(app):
    from flask_app.extensions import db, login_manager
    db.init_app(app)
    with app.app_context():
        # Create tables, if necessary. Does not update tables if already present
        db.create_all()

    login_manager.init_app(app)
    # with app.app_context():
    #     # When user accesses a page unauthorized, redirect them to home
    #     from flask import url_for
    #     from flask import redirect
    #     login_manager.unauthorized_handler(redirect("/"))


def register_blueprints(app):
    from flask_app import auth, main

    app.register_blueprint(auth.views.auth)
    app.register_blueprint(main.views.main)

    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")
