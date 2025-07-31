from app.azure_keyvault import get_secret

CLIENT_ID = get_secret("client-id")
CLIENT_SECRET = get_secret("client-secret")
TENANT_ID = get_secret("tenant-id")
TEACHERS_GROUP_ID = get_secret("teachers-group-id")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/login"  # Must match Azure AD redirect URI
SCOPES = ["User.Read"]
SESSION_TYPE = "filesystem"
