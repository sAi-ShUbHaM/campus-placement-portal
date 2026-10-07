from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        role = request.form["role"]

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO users
            (name, email, password, phone, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            phone,
            role
        ))

        connection.commit()
        connection.close()

        return "Registration successful!"

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user is None:
            return "Invalid email or password"

        if not check_password_hash(user["password"], password):
            return "Invalid email or password"

        session["user_id"] = user["id"]
        session["role"] = user["role"]

        if user["role"] == "student":
            return redirect(url_for("student.student_dashboard"))

        elif user["role"] == "recruiter":
            return redirect(url_for("recruiter.recruiter_dashboard"))

        elif user["role"] == "admin":
            return redirect(url_for("admin.admin_dashboard"))

        return "Invalid role"

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))

