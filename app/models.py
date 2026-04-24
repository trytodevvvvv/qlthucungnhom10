from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='customer') # admin, receptionist, veterinarian, customer
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(20))
    plain_password = db.Column(db.String(100))  # Lưu mật khẩu gốc để hiển thị
    is_active = db.Column(db.Boolean, default=True)
    
    # Link to customer if role is 'customer'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer_profile = db.relationship('Customer', backref=db.backref('user_account', uselist=False))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, index=True, nullable=False)
    address = db.Column(db.String(200))
    tier = db.Column(db.String(20), default='Standard') # Standard, Silver, Gold, Platinum, Diamond, VIP
    points = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    pets = db.relationship('Pet', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def update_tier(self):
        from app.models import Order
        total = db.session.query(db.func.sum(Order.total_amount)).filter_by(customer_id=self.id).scalar() or 0
        self.total_spent = total
        
        if total >= 50000000:
            self.tier = 'VIP'
        elif total >= 20000000:
            self.tier = 'Diamond'
        elif total >= 10000000:
            self.tier = 'Platinum'
        elif total >= 4000000:
            self.tier = 'Gold'
        elif total >= 2000000:
            self.tier = 'Silver'
        else:
            self.tier = 'Standard'
        db.session.commit()

class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50)) # Chó, Mèo...
    breed = db.Column(db.String(50))
    dob = db.Column(db.Date)
    weight = db.Column(db.Float)
    image = db.Column(db.String(200))
    health_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    products = db.relationship('Product', backref='category', lazy='dynamic')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    sku = db.Column(db.String(50), unique=True, index=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float)
    stock_quantity = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)

class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    services = db.relationship('PetService', backref='category', lazy='dynamic')

class PetService(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    is_active = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Optional groomer
    booking_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Confirmed, In Progress, Completed, Cancelled
    is_paid = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    customer = db.relationship('Customer', backref='bookings')
    pet = db.relationship('Pet', backref='bookings')
    service = db.relationship('PetService', backref='bookings')
    employee = db.relationship('User', backref='assigned_bookings')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id')) # Optional 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Cashier
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50)) # Cash, Banking, POS
    status = db.Column(db.String(20), default='Completed')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    customer = db.relationship('Customer', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Price at time of order

class Voucher(db.Model):
    __tablename__ = 'vouchers'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, index=True, nullable=False)
    discount_amount = db.Column(db.Float, nullable=False) # Số tiền giảm
    discount_type = db.Column(db.String(20), default='fixed') # fixed or percentage
    min_order_amount = db.Column(db.Float, default=0)
    min_tier = db.Column(db.String(20), default='Gold') # Hạng tối thiểu được dùng
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
