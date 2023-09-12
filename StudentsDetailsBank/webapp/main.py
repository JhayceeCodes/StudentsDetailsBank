from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/home", methods=["GET","POST"])
@main.route("/", methods=["GET","POST"])
def home():
    if request.method=="POST":
        return redirect(url_for(".details"))
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/student-info", methods=["GET","POST"])
@login_required
def details():
    if request.method=="POST":
        return redirect(url_for("update.update_info"))
    return render_template(
        "details.html",
        name=current_user.name,
        university=current_user.info.university,
        campus=current_user.info.campus,
        faculty=current_user.info.faculty,
        department=current_user.info.department,
        matric_number=current_user.matric_number,
        DOB=current_user.info.DOB,
        Email=current_user.info.Email,
        courses=current_user.info.courses,
        others=current_user.info.others,
    )
