from flask import Flask
from flask_session import Session
from app.config import *
from app.routes import main_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = "super-secret-key"  # Replace with secure secret in production

    # Load Azure AD config from config.py (dynamic values for SERVER_NAME, REDIRECT_PATH, AUTHORITY)
    app.config['CLIENT_ID'] = CLIENT_ID
    app.config['CLIENT_SECRET'] = CLIENT_SECRET
    app.config['TENANT_ID'] = TENANT_ID
    app.config['SERVER_NAME'] = SERVER_NAME
    app.config['REDIRECT_PATH'] = REDIRECT_PATH
    app.config['AUTHORITY'] = AUTHORITY

    app.config['SCOPES'] = SCOPES
    app.config['SESSION_TYPE'] = SESSION_TYPE  # should be 'filesystem'

    # Debug print to confirm loaded config
    print("Loaded CLIENT_ID from config:", app.config['CLIENT_ID'])
    print("Using SERVER_NAME:", app.config['SERVER_NAME'])
    print("Using REDIRECT_PATH:", app.config['REDIRECT_PATH'])
    print("Using AUTHORITY:", app.config['AUTHORITY'])

    # Initialize session
    Session(app)

    # Register blueprint(s)
    app.register_blueprint(main_routes)

    return app
