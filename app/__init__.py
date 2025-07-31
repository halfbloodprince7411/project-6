from flask import Flask
from flask_session import Session  # ✅ Add this
from app.config import *
from app.routes import main_routes  # Import blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = "super-secret-key"  # Replace with secure secret in production

    # Load Azure AD config
    app.config['CLIENT_ID'] = CLIENT_ID
    app.config['CLIENT_SECRET'] = CLIENT_SECRET
    app.config['TENANT_ID'] = TENANT_ID
    app.config['AUTHORITY'] = AUTHORITY
    app.config['REDIRECT_PATH'] = REDIRECT_PATH
    app.config['SCOPES'] = SCOPES
    app.config['SESSION_TYPE'] = SESSION_TYPE  # should be 'filesystem'
    app.config['SERVER_NAME'] = 'localhost:5001'

     # Debug print to confirm secret loaded
    print("Loaded CLIENT_ID from config:", app.config['CLIENT_ID'])

    # ✅ Initialize session
    Session(app)

    # Register blueprints
    app.register_blueprint(main_routes)

    return app
