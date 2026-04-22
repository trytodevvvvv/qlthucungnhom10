import sqlalchemy
import os
from sqlalchemy import create_engine
from app import create_app, db
from app.models import User, Customer, Pet, Category, Product, ServiceCategory, PetService, Booking, Order, OrderItem

def init_db():
    app = create_app()
    
    # Extract db info from URI
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    
    if db_uri.startswith('mysql'):
        base_uri = db_uri.rsplit('/', 1)[0]
        db_name = db_uri.rsplit('/', 1)[1]
        
        try:
            engine = create_engine(base_uri)
            with engine.connect() as conn:
                conn.execute(sqlalchemy.text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Đã kiểm tra/khởi tạo cơ sở dữ liệu: {db_name}")
        except Exception as e:
            print(f"❌ Lỗi database: {str(e)}")
            return
            
    with app.app_context():
        db.create_all()
        print("✅ Data tables created/verified!")

        # 1. Admin User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("📝 Tạo tài khoản admin...")
            admin = User(username='admin', role='admin')
            admin.set_password('123456')
            db.session.add(admin)
        
        # 2. Staff
        if not User.query.filter_by(username='groomer1').first():
            groomer = User(username='groomer1', role='groomer')
            groomer.set_password('123456')
            db.session.add(groomer)

        # 3. Customer & Pets
        if Customer.query.count() == 0:
            print("📝 Thêm khách hàng và thú cưng mẫu...")
            c1 = Customer(name="Nguyễn Văn A", phone="0988123456", tier="Silver", points=150)
            c2 = Customer(name="Trần Thị B", phone="0912345678", tier="Gold", points=300)
            db.session.add_all([c1, c2])
            db.session.commit()
            
            p1 = Pet(owner=c1, name="Milo", species="Chó", breed="Corgi", weight=12.5)
            p2 = Pet(owner=c1, name="Bông", species="Mèo", breed="Ba Tư", weight=4.2)
            p3 = Pet(owner=c2, name="Mực", species="Chó", breed="Poodle", weight=5.0)
            db.session.add_all([p1, p2, p3])
        
        # 4. Product Categories & Products
        if Category.query.count() == 0:
            print("📝 Thêm danh mục và sản phẩm mẫu...")
            cat_food = Category(name="Thức ăn", description="Thức ăn khô và ướt cho thú cưng")
            cat_acc = Category(name="Phụ kiện", description="Vòng cổ, dây dắt, lồng vận chuyển")
            cat_toy = Category(name="Đồ chơi", description="Xương gặm, cần câu mèo, bóng")
            db.session.add_all([cat_food, cat_acc, cat_toy])
            db.session.commit()

            products = [
                Product(name="Hạt Royal Canin Puppy 2kg", sku="RC-P-2000", price=450000, cost=350000, stock_quantity=15, category=cat_food),
                Product(name="Pate Whiskas Vị Cá Thu 85g", sku="WK-M-085", price=15000, cost=10000, stock_quantity=50, category=cat_food),
                Product(name="Vòng cổ phản quang", sku="ACC-CO-01", price=45000, cost=20000, stock_quantity=20, category=cat_acc),
                Product(name="Sữa tắm SOS 500ml", sku="ACC-SH-01", price=120000, cost=80000, stock_quantity=12, category=cat_acc),
                Product(name="Cần câu mèo lông vũ", sku="TOY-C-01", price=35000, cost=15000, stock_quantity=5, category=cat_toy)
            ]
            db.session.add_all(products)

        # 5. Service Categories & Services
        if ServiceCategory.query.count() == 0:
            print("📝 Thêm dịch vụ mẫu...")
            scat_groom = ServiceCategory(name="Làm đẹp (Grooming)")
            scat_health = ServiceCategory(name="Sức khỏe")
            db.session.add_all([scat_groom, scat_health])
            db.session.commit()

            services = [
                PetService(name="Tắm sấy cơ bản (Chó nhỏ)", price=150000, duration_minutes=45, category=scat_groom),
                PetService(name="Cắt tỉa tạo kiểu (Chó nhỏ)", price=350000, duration_minutes=90, category=scat_groom),
                PetService(name="Cắt móng & vệ sinh tai", price=50000, duration_minutes=15, category=scat_groom),
                PetService(name="Tiêm ngừa dại (Rabies)", price=120000, duration_minutes=10, category=scat_health)
            ]
            db.session.add_all(services)

        db.session.commit()
        print("✅ Toàn bộ dữ liệu mẫu đã được nạp thành công!")

if __name__ == '__main__':
    init_db()
