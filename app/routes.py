import msal
from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from .auth import is_teacher_claims  # Updated role check for claims
from .data import get_students

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
    print("🔑 /login route hit")
    print("SERVER_NAME:", current_app.config['SERVER_NAME'])
    print("REDIRECT_PATH:", current_app.config['REDIRECT_PATH'])
    redirect_uri = url_for("main_routes.authorized", _external=True)
    print("Redirect URI being sent:", redirect_uri)

    msal_app = _build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=current_app.config['SCOPES'],
        redirect_uri=redirect_uri
    )
    return redirect(auth_url)

# MSAL callback endpoint
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

    # DEBUG: print user claims and roles from the token
    print("DEBUG: User claims stored in session:", session["user"])
    print("DEBUG: Groups from token:", session["user"].get("groups", []))
    user_roles = session["user"].get("roles", [])
    print("DEBUG: Roles from token:", user_roles)

    # Redirect based on role/group claim
    if is_teacher_claims(session["user"]):
        print("User identified as teacher.")
        return redirect(url_for("main_routes.teacher"))
    else:
        print("User NOT identified as teacher.")
        return redirect(url_for("main_routes.student"))

@main_routes.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri="
        + url_for("main_routes.login", _external=True)
    )

# Protected teacher page
@main_routes.route("/teacher")
def teacher():
    user = session.get("user")
    if not user:
        return redirect(url_for("main_routes.login"))
    
    if not is_teacher_claims(user):
        return render_template("student.html", user=user, teacher=False)

    students = get_students()  # Call function here to get list
    return render_template("teacher.html", user=user, students=students)

# Student page (open to logged-in users who are not teachers)
@main_routes.route("/student")
def student():
    user = session.get("user")
    if not user:
        return redirect(url_for("main_routes.login"))
    return render_template("student.html", user=user)


@main_routes.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")

@main_routes.route("/debug-secrets")
def debug_secrets():
    from app.azure_keyvault import get_secret
    try:
        client_id = get_secret("client-id")
        tenant_id = get_secret("tenant-id")
        return f"✅ Successfully fetched secrets.<br>CLIENT_ID: {client_id}<br>TENANT_ID: {tenant_id}"
    except Exception as e:
        return f"❌ Error fetching secrets from Key Vault: {e}"

