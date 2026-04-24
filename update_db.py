from app import create_app
from app.extensions import db
from app.models import Customer, Voucher
from sqlalchemy import text

app = create_app()
with app.app_context():
    # 1. Add total_spent column if not exists
    try:
        db.session.execute(text("ALTER TABLE customers ADD COLUMN total_spent FLOAT DEFAULT 0.0"))
        print("Added total_spent column to customers table")
    except Exception as e:
        print("Column total_spent might already exist or error:", e)

    # 2. Create tables (vouchers)
    try:
        db.create_all()
        print("Database schema updated (vouchers table created if missing)")
    except Exception as e:
        print("Error in create_all:", e)

    # 3. Reset all customer tiers to Standard
    try:
        customers = Customer.query.all()
        for c in customers:
            c.tier = 'Standard'
        db.session.commit()
        print(f"Reset tier to Standard for {len(customers)} customers")
    except Exception as e:
        print("Error resetting tiers:", e)

    # 4. Seed sample vouchers
    try:
        if not Voucher.query.filter_by(code='GOLD5').first():
            db.session.add(Voucher(code='GOLD5', discount_amount=5.0, discount_type='percentage', min_tier='Gold'))
        if not Voucher.query.filter_by(code='PLATINUM10').first():
            db.session.add(Voucher(code='PLATINUM10', discount_amount=10.0, discount_type='percentage', min_tier='Platinum'))
        if not Voucher.query.filter_by(code='VIP20').first():
            db.session.add(Voucher(code='VIP20', discount_amount=20.0, discount_type='percentage', min_tier='VIP'))
        
        db.session.commit()
        print("Seeded sample vouchers (GOLD5, PLATINUM10, VIP20)")
    except Exception as e:
        print("Error seeding vouchers:", e)

print("Database update complete!")
