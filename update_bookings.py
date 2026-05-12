from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE bookings ADD COLUMN is_paid BOOLEAN DEFAULT FALSE"))
        db.session.commit()
        print("Added is_paid column to bookings table")
    except Exception as e:
        print("Column is_paid might already exist or error:", e)
