from app import create_app, db
from app.models import Student  # 👈 make sure this is imported

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
