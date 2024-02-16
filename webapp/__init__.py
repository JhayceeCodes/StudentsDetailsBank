from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path, getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Create SQLAlchemy instance
db = SQLAlchemy()

DB_NAME = "new_database.db"

def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.secret_key = getenv("SECRET_KEY", "default_secret_key")  # Provide a default value if SECRET_KEY is not set
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    from .models import Student, Info  # Import inside the function

    from .main import main
    from .auth import auth
    from .update import update

    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(update, url_prefix="/")

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists("webblog/" + "students_database"):
            db.create_all()
            print("Database created")
