import msal
from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from .auth import is_teacher_claims
from .data import get_students  # remove get_teachers import since no longer needed
from app.models import Student, Teacher
from app.models import Student
from app import db
import logging

logging.basicConfig(level=logging.DEBUG)


logging.basicConfig(level=logging.DEBUG)

main_routes = Blueprint('main_routes', __name__)

# MSAL helpers

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        current_app.config['CLIENT_ID'],
        authority=current_app.config['AUTHORITY'],
        client_credential=current_app.config['CLIENT_SECRET'],
        token_cache=cache
    )

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

@main_routes.route("/")
def index():
    return redirect(url_for("main_routes.login"))

# Replace old /login with MSAL login flow
@main_routes.route("/login")
def login():
    print("🔑 /login route hit", flush=True)
    print(f"SERVER_NAME: {current_app.config.get('SERVER_NAME')}", flush=True)
    print(f"REDIRECT_PATH: {current_app.config.get('REDIRECT_PATH')}", flush=True)

    redirect_uri = url_for("main_routes.authorized", _external=True)
    print(f"Redirect URI being sent: {redirect_uri}", flush=True)

    msal_app = _build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=current_app.config['SCOPES'],
        redirect_uri=redirect_uri
    )
    return redirect(auth_url)




@main_routes.route("/authorized")
def authorized():
    cache = _load_cache()
    msal_app = _build_msal_app(cache)

    code = request.args.get("code")
    if not code:
        return redirect(url_for("main_routes.login"))

    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=current_app.config['SCOPES'],
        redirect_uri=url_for("main_routes.authorized", _external=True)
    )

    if "error" in result:
        return f"Login failure: {result.get('error_description')}"

    # Store user claims in session
    session["user"] = result.get("id_token_claims")
    _save_cache(cache)

    user = session["user"]
    is_teacher = is_teacher_claims(user)

    print("DEBUG: User claims stored in session:", user)
    print("DEBUG: Groups from token:", user.get("groups", []))
    print("DEBUG: Roles from token:", user.get("roles", []))
    print(f"User identified as {'teacher' if is_teacher else 'student'}.")

    # Redirect to unified students page, which handles role-based view
    return redirect(url_for("main_routes.students"))


@main_routes.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri="
        + url_for("main_routes.login", _external=True)
    )

# Protected teacher page
@main_routes.route("/teachers")
def teachers():
    user = session.get("user")
    if not user:
        return redirect(url_for("main_routes.login"))

    if not is_teacher_claims(user):
        return redirect(url_for("main_routes.unauthorized"))

    teachers_list = Teacher.query.all()

    return render_template("teachers.html", user=user, teachers=teachers_list)



@main_routes.route("/students")
def students():
    user = session.get("user")
    if not user:
        return redirect(url_for("main_routes.login"))

    is_teacher = is_teacher_claims(user)
    all_students = Student.query.all()

    return render_template("students.html", user=user, students=all_students, is_teacher=is_teacher)


# TEMP route for testing
@main_routes.route("/debug/students")
def debug_students():
    from app.models import Student
    all_students = Student.query.all()
    return f"Found {len(all_students)} students"

@main_routes.route("/debug/seed-students")
def seed_students():
    from app import db
    from app.models import Student

    students = [
        Student(name="Harry Potter", email="harry@hogwarts.edu"),
        Student(name="Hermione Granger", email="hermione@hogwarts.edu"),
        Student(name="Ron Weasley", email="ron@hogwarts.edu")
    ]

    db.session.bulk_save_objects(students)
    db.session.commit()
    return "Sample students inserted."




@main_routes.route("/debug-secrets")
def debug_secrets():
    user = session.get("user")
    if not user or not is_teacher_claims(user):
        return redirect(url_for("main_routes.unauthorized"))

    from app.azure_keyvault import get_secret
    try:
        client_id = get_secret("client-id")
        tenant_id = get_secret("tenant-id")
        return f"✅ Successfully fetched secrets.<br>CLIENT_ID: {client_id}<br>TENANT_ID: {tenant_id}"
    except Exception as e:
        return f"❌ Error fetching secrets from Key Vault: {e}"

@main_routes.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")

