# test_db_connection.py

from app import create_app, db
from sqlalchemy import text  # ✅ import text

app = create_app()

with app.app_context():
    try:
        # ✅ Wrap raw SQL string in text()
        result = db.session.execute(text("SELECT 1"))
        print("✅ Database connection successful. Result:", result.scalar())
    except Exception as e:
        print("❌ Database connection failed:", str(e))
