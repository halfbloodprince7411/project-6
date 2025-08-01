import os
from app.azure_keyvault import get_secret

SQL_CONNECTION_STRING = get_secret("DbConnectionString")


# Secure secrets from Azure Key Vault
CLIENT_ID = get_secret("client-id")
CLIENT_SECRET = get_secret("client-secret")
TENANT_ID = get_secret("tenant-id")
TEACHERS_GROUP_ID = get_secret("teachers-group-id")

# Common settings
SCOPES = ["User.Read"]
SESSION_TYPE = "filesystem"

# Environment-based settings
if os.getenv("AZURE_ENV") == "PRODUCTION":
    SERVER_NAME = "ncpl-training-app-47fb6d.azurewebsites.net"
    REDIRECT_PATH = "/authorized"
    REDIRECT_URI = f"https://{SERVER_NAME}{REDIRECT_PATH}"
else:
    SERVER_NAME = "localhost:5001"
    REDIRECT_PATH = "/login"
    REDIRECT_URI = f"http://{SERVER_NAME}{REDIRECT_PATH}"


# Final AUTHORITY depends on TENANT_ID
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
