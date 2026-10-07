from flask import Blueprint, render_template, session, redirect, url_for, abort
from database import get_db_connection

admin_bp = Blueprint("admin", __name__)


# =========================
# ADMIN DASHBOARD
# =========================

@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        abort(403)

    connection = get_db_connection()

    # Pending companies
    companies = connection.execute("""
        SELECT *
        FROM companies
        WHERE approval_status = 'PENDING'
    """).fetchall()

    # Pending jobs
    jobs = connection.execute("""
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies
        ON jobs.company_id = companies.id
        WHERE jobs.approval_status = 'PENDING'
    """).fetchall()

    connection.close()

    return render_template(
        "admin_dashboard.html",
        companies=companies,
        jobs=jobs
    )


# =========================
# APPROVE COMPANY
# =========================

@admin_bp.route("/admin/company/<int:company_id>/approve", methods=["POST"])
def approve_company(company_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        abort(403)

    connection = get_db_connection()

    connection.execute("""
        UPDATE companies
        SET approval_status = 'APPROVED'
        WHERE id = ?
    """, (company_id,))

    connection.execute("""
        INSERT INTO audit_logs
        (admin_id, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        "APPROVED",
        "COMPANY",
        company_id,
        "Company approved by admin"
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("admin.admin_dashboard"))


# =========================
# REJECT COMPANY
# =========================

@admin_bp.route("/admin/company/<int:company_id>/reject", methods=["POST"])
def reject_company(company_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        abort(403)

    connection = get_db_connection()

    connection.execute("""
        UPDATE companies
        SET approval_status = 'REJECTED'
        WHERE id = ?
    """, (company_id,))

    connection.execute("""
        INSERT INTO audit_logs
        (admin_id, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        "REJECTED",
        "COMPANY",
        company_id,
        "Company rejected by admin"
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("admin.admin_dashboard"))


# =========================
# APPROVE JOB
# =========================

@admin_bp.route("/admin/job/<int:job_id>/approve", methods=["POST"])
def approve_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        abort(403)

    connection = get_db_connection()

    connection.execute("""
        UPDATE jobs
        SET approval_status = 'APPROVED'
        WHERE id = ?
    """, (job_id,))

    connection.execute("""
        INSERT INTO audit_logs
        (admin_id, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        "APPROVED",
        "JOB",
        job_id,
        "Job approved by admin"
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("admin.admin_dashboard"))


# =========================
# REJECT JOB
# =========================

@admin_bp.route("/admin/job/<int:job_id>/reject", methods=["POST"])
def reject_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        abort(403)

    connection = get_db_connection()

    connection.execute("""
        UPDATE jobs
        SET approval_status = 'REJECTED'
        WHERE id = ?
    """, (job_id,))

    connection.execute("""
        INSERT INTO audit_logs
        (admin_id, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        "REJECTED",
        "JOB",
        job_id,
        "Job rejected by admin"
    ))

    connection.commit()
    connection.close()

    return redirect(url_for("admin.admin_dashboard"))