from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import current_user, login_required
from . import db
from .models import Info


update = Blueprint("update", __name__)

@update.route("/update_info", methods=["GET","POST"])
@login_required
def update_info():
    if request.method=="POST":
        courses1 = request.form.get("courses")
        others1 = request.form.get("others")
        current_user.info.courses=courses1
        current_user.info.others=others1
        db.session.commit()
        flash("Information successfully updated", category="success")
        return redirect(url_for("main.details"))
    return render_template(
            "update.html",
            courses = current_user.info.courses,
            others = current_user.info.others,
            )
