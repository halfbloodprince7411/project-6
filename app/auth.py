from flask import current_app
from app.config import TEACHERS_GROUP_ID

def is_teacher_claims(claims):
    user_groups = claims.get("groups", [])
    print("🔍 User groups:", user_groups)
    print("🔑 Teachers group ID from config:", TEACHERS_GROUP_ID)

    return TEACHERS_GROUP_ID in user_groups
