import sqlalchemy
import os
from sqlalchemy import create_engine
from app import create_app, db
from app.models import User, Customer, Pet

def init_db():
    app = create_app()
    
    # Extract db info from URI
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    # e.g. mysql+pymysql://root:@127.0.0.1/petshop_db
    
    if db_uri.startswith('mysql'):
        base_uri = db_uri.rsplit('/', 1)[0] # 'mysql+pymysql://root:@127.0.0.1'
        db_name = db_uri.rsplit('/', 1)[1]
        
        try:
            engine = create_engine(base_uri)
            with engine.connect() as conn:
                conn.execute(sqlalchemy.text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Đã kiểm tra/khởi tạo cơ sở dữ liệu: {db_name}")
        except Exception as e:
            print(f"❌ Không thể tạo database tự động. Vui lòng đảm bảo Laragon đang chạy và thử lại. Lỗi cụ thể: {str(e)}")
            return
            
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Data tables created!")

        # Check if admin user exists
        if not User.query.filter_by(username='admin').first():
            print("📝 Tạo tài khoản admin mặc định...")
            admin = User(username='admin', role='admin')
            admin.set_password('123456')
            db.session.add(admin)
            
            # Dummy Data
            print("📝 Thêm thông tin dummy data...")
            c1 = Customer(name="Nguyễn Văn A", phone="0988123456", tier="Silver", points=150)
            c2 = Customer(name="Trần Thị B", phone="0912345678", tier="Gold", points=300)
            db.session.add(c1)
            db.session.add(c2)
            db.session.commit() # commit customers to get unqiue IDs
            
            p1 = Pet(owner=c1, name="Milo", species="Chó", breed="Corgi", weight=12.5)
            p2 = Pet(owner=c1, name="Bông", species="Mèo", breed="Ba Tư", weight=4.2)
            p3 = Pet(owner=c2, name="Mực", species="Chó", breed="Poodle", weight=5.0)
            db.session.add_all([p1, p2, p3])
            
            db.session.commit()
            print("✅ Admin account: admin / 123456")
        else:
            print("ℹ️ Dummy data đã tồn tại.")

if __name__ == '__main__':
    init_db()
