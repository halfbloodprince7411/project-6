from flask import Flask
from flask_session import Session
from app.config import *
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
import urllib

db = SQLAlchemy()  # ✅ Initialize globally

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.secret_key = "super-secret-key"

    # Load configs
    app.config['CLIENT_ID'] = CLIENT_ID
    app.config['CLIENT_SECRET'] = CLIENT_SECRET
    app.config['TENANT_ID'] = TENANT_ID
    app.config['SERVER_NAME'] = SERVER_NAME
    app.config['REDIRECT_PATH'] = REDIRECT_PATH
    app.config['AUTHORITY'] = AUTHORITY
    app.config['SCOPES'] = SCOPES
    app.config['SESSION_TYPE'] = SESSION_TYPE

    # DB config
    params = urllib.parse.quote_plus(SQL_CONNECTION_STRING)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Session(app)

    # ✅ Import routes **after** db.init_app to avoid circular import
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app
