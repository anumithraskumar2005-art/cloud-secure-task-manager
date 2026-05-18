from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt, limiter
from app.models import User, Task, LoginLog

main = Blueprint("main", __name__)
UPLOAD_FOLDER = "app/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "docx", "txt"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/health")
def health():
    return {
        "status": "ok",
        "service": "secure-task-manager",
        "database": "connected"
    }

@main.route("/")
def home():
    return render_template("home.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("main.register"))

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        ip_address = request.remote_addr

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            log = LoginLog(email=email, ip_address=ip_address, status="success")
            db.session.add(log)
            db.session.commit()

            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.dashboard"))

        log = LoginLog(email=email, ip_address=ip_address, status="failed")
        db.session.add(log)
        db.session.commit()

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@main.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    total_tasks = len(tasks)
    todo_tasks = len([task for task in tasks if task.status == "To Do"])
    progress_tasks = len([task for task in tasks if task.status == "In Progress"])
    completed_tasks = len([task for task in tasks if task.status == "Completed"])

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total_tasks=total_tasks,
        todo_tasks=todo_tasks,
        progress_tasks=progress_tasks,
        completed_tasks=completed_tasks
    )


@main.route("/add-task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")
        uploaded_file = request.files.get("attachment")

        filename = None

        if uploaded_file and uploaded_file.filename != "":
            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                uploaded_file.save(file_path)
            else:
                flash("Invalid file type. Allowed: png, jpg, jpeg, pdf, docx, txt.", "danger")
                return redirect(url_for("main.add_task"))

        task = Task(
            title=title,
            description=description,
            status=status,
            attachment=filename,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task created successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("add_task.html")


@main.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash("You are not allowed to edit this task.", "danger")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        task.title = request.form.get("title")
        task.description = request.form.get("description")
        task.status = request.form.get("status")

        uploaded_file = request.files.get("attachment")

        if uploaded_file and uploaded_file.filename != "":
            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                uploaded_file.save(file_path)
                task.attachment = filename
            else:
                flash("Invalid file type. Allowed: png, jpg, jpeg, pdf, docx, txt.", "danger")
                return redirect(url_for("main.edit_task", task_id=task.id))

        db.session.commit()

        flash("Task updated successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_task.html", task=task)


@main.route("/delete-task/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash("You are not allowed to delete this task.", "danger")
        return redirect(url_for("main.dashboard"))

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully.", "success")
    return redirect(url_for("main.dashboard"))


@main.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("main.dashboard"))

    users = User.query.all()
    tasks = Task.query.all()
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(10).all()

    total_users = len(users)
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.status == "Completed"])
    failed_logins = len([log for log in logs if log.status == "failed"])

    return render_template(
        "admin.html",
        users=users,
        tasks=tasks,
        logs=logs,
        total_users=total_users,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        failed_logins=failed_logins
    )


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("main.login"))