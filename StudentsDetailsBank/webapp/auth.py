from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import Student, Info
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        matric_number = request.form.get("matriculation")
        password = request.form.get("password")

        student = Student.query.filter_by(matric_number=matric_number).first()
        if student:
            if check_password_hash(student.password, password):
                login_user(student, remember=True)
                if current_user.info:
                    flash("Login Succesfull", category="success")
                    return redirect(url_for("main.details"))
                else:
                    flash("You are yet to fill in your information", category="message")
                    return redirect(url_for(".register"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Matriculation number does not exist", category="error")

    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
       name = request.form.get("name")
       matric_number = request.form.get("matric_number")
       password1 = request.form.get("password1")
       password2 = request.form.get("password2") 
       name_exists = Student.query.filter_by(name=name).first()
       matricNumber_exists = Student.query.filter_by(matric_number=matric_number).first()

       if name_exists:
            flash("Name already in use", category="error")
       elif matricNumber_exists:
            flash("Matric number is already in use", category="error")
       elif password1 != password2:
            flash("Passwords don't match", category="error")
       else:
            new_student = Student(
                name = name,
                matric_number = matric_number,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_student)
            db.session.commit()
            login_user(new_student, remember=True) 
            return redirect(url_for(".login")) 


    return render_template("signup.html")


@auth.route("/store-info", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        campus = request.form.get("campus")
        faculty = request.form.get("faculty")
        department = request.form.get("department")
        Email = request.form.get("Email")
        DOB = request.form.get("DOB")
        courses = request.form.get("courses")
        others = request.form.get("others")
        university = request.form.get("university_name")
        emailValidRegex=re.compile(r"[a-zA-Z0-9._%+-]+@+[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")

        if not emailValidRegex.search(Email):
            flash("The email provided is invalid, please ensure you fill in the correct one", category="error")
       
        else:
            new_info = Info(
                university=university,
                campus=campus,
                faculty=faculty,
                department=department,
                DOB=DOB,
                Email=Email,
                others=others,
                courses=courses,
                student=current_user
            )
            db.session.add(new_info)
            db.session.commit()
            flash("Student successfully registered")
            return redirect(url_for("auth.login"))

    return render_template("store-info.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
