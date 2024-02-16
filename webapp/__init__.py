from flask import Flask #current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from datetime import timedelta
import os
from dotenv import load_dotenv
from .models import Student, Info

db = SQLAlchemy()
DB_NAME = "new_database.db"
load_dotenv(".env")

def create_app():
    app=Flask(__name__, template_folder="templates")
    #app.permanent_session_lifetime = timedelta(minutes=5)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    #app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+pymysql://username:yourmysqlpassword@host/database"
    #^^^optional if you wish to use mysql
    app.secret_key: str = os.getenv("SECRET_KEY") # here i used an environment variable to store my secret key, so you can create one and utilize in the same manner...
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

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
