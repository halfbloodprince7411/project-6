import os
from app.azure_keyvault import get_secret

CLIENT_ID = get_secret("client-id")
CLIENT_SECRET = get_secret("client-secret")
TENANT_ID = get_secret("tenant-id")
TEACHERS_GROUP_ID = get_secret("teachers-group-id")


# Detect environment
if os.getenv("AZURE_ENV") == "PRODUCTION":
    SERVER_NAME = "ncpl-training-app-47fb6d.azurewebsites.net"
    REDIRECT_PATH = "/authorized"
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
else:
    SERVER_NAME = "localhost:5001"
    REDIRECT_PATH = "/authorized"



AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/login"  # Must match Azure AD redirect URI
SCOPES = ["User.Read"]
SESSION_TYPE = "filesystem"
