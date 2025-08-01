from app import create_app, db
from app.models import Teacher

app = create_app()

with app.app_context():
    # Ensure tables exist
    db.create_all()

    # Seed Teacher 01 if not already present
    email = "teacher01@pemmrajusirishaoutlook.onmicrosoft.com"
    existing = Teacher.query.filter_by(email=email).first()
    if existing:
        print("✅ Teacher already exists:", existing)
    else:
        teacher = Teacher(name="Teacher 01", email=email)
        db.session.add(teacher)
        db.session.commit()
        print("✅ Inserted Teacher 01")
