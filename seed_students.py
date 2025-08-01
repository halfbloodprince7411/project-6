from app import create_app, db
from app.models import Student

app = create_app()

with app.app_context():
    # Ensure tables exist
    db.create_all()

    # Check if students already exist to avoid duplicates
    existing_students = Student.query.all()
    if existing_students:
        print(f"✅ {len(existing_students)} students already exist.")
    else:
        students = [
            Student(name="Harry Potter", email="harry@hogwarts.edu"),
            Student(name="Hermione Granger", email="hermione@hogwarts.edu"),
            Student(name="Ron Weasley", email="ron@hogwarts.edu"),
        ]
        db.session.bulk_save_objects(students)
        db.session.commit()
        print("✅ Inserted 3 students")
