from flask import Blueprint, render_template, request, redirect, session, flash
from database import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/note&do/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")

    # POST
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if register_user(name, email, password):
        flash("Registration successful! Please login.", "success")
        return redirect("/note&do/auth/login")


    flash("Registration failed! Email may already exist.", "danger")
    return redirect("/note&do/auth/register")


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")

    user = login_user(email, password)
    if user:
        flash(f"Welcome back, {user['name']}!", "success")
        session["uid"] = user["uid"]
        session["name"] = user["name"]
      
        return redirect("/note&do/todo/")

    flash("Login failed! Check email/password.", "danger")
    return redirect("/note&do/auth/login")


@auth_bp.route("/logout")
def logout():
    flash("Logged out", "info")
    session.clear()
    return redirect("/note&do/auth/login")


