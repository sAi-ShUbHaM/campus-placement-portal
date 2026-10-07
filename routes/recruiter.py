from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from database import get_db_connection

recruiter_bp = Blueprint("recruiter", __name__)


# =========================
# RECRUITER DASHBOARD
# =========================

@recruiter_bp.route("/recruiter/dashboard")
def recruiter_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "recruiter":
        abort(403)

    connection = get_db_connection()

    # Get recruiter details
    recruiter = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    # Get recruiter's company
    company = connection.execute(
        "SELECT * FROM companies WHERE recruiter_id = ?",
        (session["user_id"],)
    ).fetchone()

    # Get all jobs created by this company
    if company:

        jobs = connection.execute("""
            SELECT *
            FROM jobs
            WHERE company_id = ?
        """, (company["id"],)).fetchall()

    else:

        jobs = []

    connection.close()

    return render_template(
        "recruiter_dashboard.html",
        recruiter=recruiter,
        company=company,
        jobs=jobs
    )


# =========================
# COMPANY PROFILE
# =========================

@recruiter_bp.route("/recruiter/company", methods=["GET", "POST"])
def recruiter_company():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "recruiter":
        abort(403)

    connection = get_db_connection()

    # Check whether company already exists
    company = connection.execute(
        "SELECT * FROM companies WHERE recruiter_id = ?",
        (session["user_id"],)
    ).fetchone()

    # If form is submitted
    if request.method == "POST":

        company_name = request.form["company_name"]
        description = request.form["description"]
        website = request.form["website"]

        # Create new company
        if company is None:

            connection.execute("""
                INSERT INTO companies
                (
                    recruiter_id,
                    company_name,
                    description,
                    website
                )
                VALUES (?, ?, ?, ?)
            """, (
                session["user_id"],
                company_name,
                description,
                website
            ))

        # Update existing company
        else:

            connection.execute("""
                UPDATE companies
                SET company_name = ?,
                    description = ?,
                    website = ?
                WHERE recruiter_id = ?
            """, (
                company_name,
                description,
                website,
                session["user_id"]
            ))

        connection.commit()
        connection.close()

        return redirect(url_for("recruiter.recruiter_dashboard"))

    connection.close()

    return render_template(
        "recruiter_company.html",
        company=company
    )


# =========================
# CREATE JOB
# =========================

@recruiter_bp.route("/recruiter/jobs/create", methods=["GET", "POST"])
def create_job():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "recruiter":
        abort(403)

    connection = get_db_connection()

    # Get recruiter's company
    company = connection.execute(
        "SELECT * FROM companies WHERE recruiter_id = ?",
        (session["user_id"],)
    ).fetchone()

    # Company doesn't exist
    if company is None:

        connection.close()

        return "Please create your company profile first."

    # Company must be approved before creating a job
    if company["approval_status"] != "APPROVED":

        connection.close()

        return "Your company must be approved before creating jobs."

    # If job form is submitted
    if request.method == "POST":

        title = request.form["title"]

        description = request.form["description"]

        minimum_cgpa = float(
            request.form["minimum_cgpa"]
        )

        allowed_departments = request.form[
            "allowed_departments"
        ]

        graduation_year = int(
            request.form["graduation_year"]
        )

        # Insert job
        connection.execute("""
            INSERT INTO jobs
            (
                company_id,
                title,
                description,
                minimum_cgpa,
                allowed_departments,
                graduation_year
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company["id"],
            title,
            description,
            minimum_cgpa,
            allowed_departments,
            graduation_year
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("recruiter.recruiter_dashboard")
        )

    connection.close()

    return render_template("create_job.html")


# =========================
# VIEW JOB CANDIDATES
# =========================

@recruiter_bp.route("/recruiter/job/<int:job_id>/candidates")
def job_candidates(job_id):

    # Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check recruiter role
    if session["role"] != "recruiter":
        abort(403)

    connection = get_db_connection()

    # Get recruiter's company
    company = connection.execute("""
        SELECT *
        FROM companies
        WHERE recruiter_id = ?
    """, (session["user_id"],)).fetchone()

    if company is None:
        connection.close()
        return "Company profile not found."

    # Get the job
    # AND company_id ensures recruiter can only
    # access jobs belonging to their own company
    job = connection.execute("""
        SELECT *
        FROM jobs
        WHERE id = ?
        AND company_id = ?
    """, (
        job_id,
        company["id"]
    )).fetchone()

    if job is None:
        connection.close()
        return "Job not found or access denied."

    # Get students who applied
    applications = connection.execute("""
        SELECT
            applications.id AS application_id,
            applications.status,
            applications.applied_at,
            applications.updated_at,

            students.branch,
            students.cgpa,
            students.graduation_year,
            students.resume_link,

            users.name,
            users.email,
            users.phone

        FROM applications

        JOIN students
            ON applications.student_id = students.id

        JOIN users
            ON students.user_id = users.id

        WHERE applications.job_id = ?

        ORDER BY applications.applied_at ASC
    """, (job_id,)).fetchall()

    connection.close()

    return render_template(
        "recruiter_candidates.html",
        job=job,
        applications=applications
    )


# =========================
# UPDATE APPLICATION STATUS
# =========================

@recruiter_bp.route(
    "/recruiter/application/<int:application_id>/status",
    methods=["POST"]
)
def update_application_status(application_id):

    # Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check recruiter role
    if session["role"] != "recruiter":
        abort(403)

    # Allowed statuses
    allowed_statuses = [
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "SELECTED",
        "REJECTED"
    ]

    new_status = request.form["status"]

    # Validate status
    if new_status not in allowed_statuses:
        return "Invalid application status."

    connection = get_db_connection()

    # Get recruiter's company
    company = connection.execute("""
        SELECT *
        FROM companies
        WHERE recruiter_id = ?
    """, (session["user_id"],)).fetchone()

    if company is None:
        connection.close()
        return "Company profile not found."

    # Find application and make sure it belongs
    # to a job posted by this recruiter
    application = connection.execute("""
        SELECT
            applications.id,
            applications.job_id
        FROM applications
        JOIN jobs
            ON applications.job_id = jobs.id
        WHERE applications.id = ?
        AND jobs.company_id = ?
    """, (
        application_id,
        company["id"]
    )).fetchone()

    if application is None:
        connection.close()
        return "Application not found or access denied."

    # Update application status
    connection.execute("""
        UPDATE applications
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        new_status,
        application_id
    ))

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "recruiter.job_candidates",
            job_id=application["job_id"]
        )
    )


# =========================
# BATCH UPDATE APPLICATION STATUS
# =========================

@recruiter_bp.route(
    "/recruiter/applications/batch-status",
    methods=["POST"]
)
def batch_update_application_status():

    # Check login
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Check recruiter role
    if session["role"] != "recruiter":
        return "Access denied"

    # Get selected applications
    application_ids = request.form.getlist("application_ids")

    # Get new status
    new_status = request.form["status"]

    # Allowed statuses
    allowed_statuses = [
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "SELECTED",
        "REJECTED"
    ]

    # Validate status
    if new_status not in allowed_statuses:
        return "Invalid application status."

    # Make sure at least one applicant is selected
    if not application_ids:
        return "Please select at least one applicant."

    connection = get_db_connection()

    # Get recruiter's company
    company = connection.execute("""
        SELECT *
        FROM companies
        WHERE recruiter_id = ?
    """, (session["user_id"],)).fetchone()

    if company is None:
        connection.close()
        return "Company profile not found."

    # Check every selected application
    # belongs to this recruiter's company
    for application_id in application_ids:

        application = connection.execute("""
            SELECT
                applications.id
            FROM applications
            JOIN jobs
                ON applications.job_id = jobs.id
            WHERE applications.id = ?
            AND jobs.company_id = ?
        """, (
            application_id,
            company["id"]
        )).fetchone()

        if application is None:
            connection.close()
            return "One or more applications are invalid or access denied."

    # Update all selected applications
    for application_id in application_ids:

        connection.execute("""
            UPDATE applications
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            new_status,
            application_id
        ))

    connection.commit()
    connection.close()

    return redirect(
        url_for("recruiter.recruiter_dashboard")
    )

