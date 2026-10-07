
from flask import Flask, render_template

from routes.auth import auth_bp
from routes.student import student_bp
from routes.recruiter import recruiter_bp
from routes.admin import admin_bp

from database import create_table


app = Flask(__name__)

app.secret_key = "campus-placement-secret-key"


app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(recruiter_bp)
app.register_blueprint(admin_bp)


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("home.html")


# =========================
# ACCESS DENIED
# =========================

@app.errorhandler(403)
def access_denied(error):
    return render_template("403.html"), 403


# =========================
# APPLICATION START
# =========================

if __name__ == "__main__":
    create_table()
    app.run(debug=True)

