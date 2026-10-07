from flask import Blueprint, render_template, request, session, redirect,url_for, abort
from database import get_db_connection

student_bp = Blueprint("student", __name__)


# =========================
# STUDENT DASHBOARD
# =========================

@student_bp.route("/student/dashboard")
def student_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "student":
        abort(403)

    message = request.args.get("message")

    connection = get_db_connection()

    # Get student user details
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    # Get student profile
    student = connection.execute(
        "SELECT * FROM students WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    # Get only APPROVED jobs
    jobs = connection.execute("""
        SELECT
            jobs.*,
            companies.company_name
        FROM jobs
        JOIN companies
        ON jobs.company_id = companies.id
        WHERE jobs.approval_status = 'APPROVED'
        AND companies.approval_status = 'APPROVED'
    """).fetchall()


    job_list = []

    for job in jobs:

        eligible, reason = check_eligibility(student, job)

        job_data = dict(job)

        job_data["eligible"] = eligible
        job_data["eligibility_reason"] = reason

        job_list.append(job_data)

    if student:

        applications = connection.execute("""
            SELECT
                applications.*,
                jobs.title,
                companies.company_name
            FROM applications
            JOIN jobs
                ON applications.job_id = jobs.id
            JOIN companies
                ON jobs.company_id = companies.id
            WHERE applications.student_id = ?
            ORDER BY applications.applied_at DESC
        """, (student["id"],)).fetchall()

    else:

        applications = []

    connection.close()


    return render_template(
        "student_dashboard.html",
        user=user,
        student=student,
        jobs=job_list,
        applications=applications,
        message=message
)


# =========================
# STUDENT PROFILE
# =========================

@student_bp.route("/student/profile", methods=["GET", "POST"])
def student_profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "student":
        abort(403)

    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    if request.method == "POST":

        branch = request.form["branch"]

        cgpa = float(
            request.form["cgpa"]
        )

        graduation_year = int(
            request.form["graduation_year"]
        )

        resume_link = request.form["resume_link"]

        # Create profile
        if student is None:

            connection.execute("""
                INSERT INTO students
                (
                    user_id,
                    branch,
                    cgpa,
                    graduation_year,
                    resume_link
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                branch,
                cgpa,
                graduation_year,
                resume_link
            ))

        # Update profile
        else:

            connection.execute("""
                UPDATE students
                SET branch = ?,
                    cgpa = ?,
                    graduation_year = ?,
                    resume_link = ?
                WHERE user_id = ?
            """, (
                branch,
                cgpa,
                graduation_year,
                resume_link,
                session["user_id"]
            ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("student.student_dashboard")
        )

    connection.close()

    return render_template(
        "student_profile.html",
        student=student
    )


# =========================
# STUDENT ELIGIBILITY CHECK
# =========================


def check_eligibility(student, job):

    if student is None:
        return False, "Please complete your student profile first."

    # Check CGPA
    if student["cgpa"] < job["minimum_cgpa"]:
        return False, (
            f"Minimum CGPA required is {job['minimum_cgpa']}. "
            f"Your CGPA is {student['cgpa']}."
        )

    # Check department
    allowed_departments = [
        dept.strip().upper()
        for dept in job["allowed_departments"].split(",")
    ]

    if student["branch"].strip().upper() not in allowed_departments:
        return False, "Your department is not eligible for this job."

    # Check graduation year
    if student["graduation_year"] != job["graduation_year"]:
        return False, (
            f"This job is for graduation year "
            f"{job['graduation_year']}."
        )

    return True, "You are eligible for this job."


# =========================
# STUDENT APPLY FOR JOB
# =========================

@student_bp.route("/student/jobs/<int:job_id>/apply", methods=["POST"])
def apply_job(job_id):

    # Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check student role
    if session["role"] != "student":
        abort(403)

    connection = get_db_connection()

    # Get student profile
    student = connection.execute(
        "SELECT * FROM students WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()

    if student is None:
        connection.close()
        return "Please complete your student profile before applying."

    # Get the job
    job = connection.execute("""
        SELECT
            jobs.*,
            companies.company_name,
            companies.approval_status AS company_approval_status
        FROM jobs
        JOIN companies
        ON jobs.company_id = companies.id
        WHERE jobs.id = ?
    """, (job_id,)).fetchone()

    if job is None:
        connection.close()
        return "Job not found."

    # Check job approval
    if job["approval_status"] != "APPROVED":
        connection.close()
        return "This job is not approved for applications."

    # Check company approval
    if job["company_approval_status"] != "APPROVED":
        connection.close()
        return "This company's approval is not valid."

    # IMPORTANT:
    # Check eligibility again on the backend
    eligible, reason = check_eligibility(student, job)

    if not eligible:
        connection.close()
        return f"You are not eligible for this job. Reason: {reason}"

    # Check whether student already applied
    existing_application = connection.execute("""
        SELECT *
        FROM applications
        WHERE student_id = ?
        AND job_id = ?
    """, (
        student["id"],
        job_id
    )).fetchone()


    if existing_application:
        connection.close()

        return redirect(
            url_for(
                "student.student_dashboard",
            message="already_applied"
        )
    )



    # Create application
    connection.execute("""
        INSERT INTO applications
        (student_id, job_id, status)
        VALUES (?, ?, 'APPLIED')
    """, (
        student["id"],
        job_id
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("student.student_dashboard"))