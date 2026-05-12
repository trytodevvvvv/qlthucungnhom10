from app import create_app
from app.extensions import db
from app.models import Customer
from sqlalchemy import text

app = create_app()
with app.app_context():
    # 1. Add total_spent column if not exists
    try:
        db.session.execute(text("ALTER TABLE customers ADD COLUMN total_spent FLOAT DEFAULT 0.0"))
        print("Added total_spent column to customers table")
    except Exception as e:
        print("Column total_spent might already exist or error:", e)

    # 2. Create tables (pets_for_sale)
    try:
        db.create_all()
        print("Database schema updated (pets_for_sale created if missing)")
    except Exception as e:
        print("Error in create_all:", e)

    # 2b. Add pet_for_sale_id to order_items
    try:
        db.session.execute(text("ALTER TABLE order_items ADD COLUMN pet_for_sale_id INTEGER"))
        db.session.execute(text("ALTER TABLE order_items ADD FOREIGN KEY (pet_for_sale_id) REFERENCES pets_for_sale(id)"))
        print("Added pet_for_sale_id column to order_items table")
    except Exception as e:
        print("Column pet_for_sale_id might already exist or error:", e)

    # 2c. Add quantity to pets_for_sale
    try:
        db.session.execute(text("ALTER TABLE pets_for_sale ADD COLUMN quantity INTEGER DEFAULT 1"))
        print("Added quantity column to pets_for_sale table")
    except Exception as e:
        print("Column quantity might already exist or error:", e)

    # 3. Reset all customer tiers to Standard
    try:
        customers = Customer.query.all()
        for c in customers:
            c.tier = 'Standard'
        db.session.commit()
        print(f"Reset tier to Standard for {len(customers)} customers")
    except Exception as e:
        print("Error resetting tiers:", e)

print("Database update complete!")
