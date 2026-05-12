from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db
from typing import Any

class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)  # type: ignore

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='receptionist') # admin, receptionist, staff, veterinarian, groomer
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(20))
    plain_password = db.Column(db.String(100))  # Lưu mật khẩu gốc để hiển thị
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(BaseModel):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, index=True, nullable=False)
    address = db.Column(db.String(200))
    points = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    pets = db.relationship('Pet', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def update_total_spent(self):
        from app.models import Order
        total = db.session.query(db.func.sum(Order.total_amount)).filter_by(customer_id=self.id).scalar() or 0
        self.total_spent = total
        db.session.commit()

class Pet(BaseModel):
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
    source = db.Column(db.String(20), default='customer_owned')  # 'customer_owned' hoặc 'store_purchase'
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)  # Liên kết đơn hàng (nếu mua từ cửa hàng)
    created_at = db.Column(db.DateTime, default=datetime.now)

    purchase_order = db.relationship('Order', backref='purchased_pets', foreign_keys=[purchase_order_id])

class PetForSale(BaseModel):
    __tablename__ = 'pets_for_sale'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50)) # Chó, Mèo...
    breed = db.Column(db.String(50))
    age = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='Available') # Available, Sold
    image = db.Column(db.String(200))
    health_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Category(BaseModel):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    products = db.relationship('Product', backref='category', lazy='dynamic')

class Product(BaseModel):
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

class ServiceCategory(BaseModel):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    services = db.relationship('PetService', backref='category', lazy='dynamic')

class PetService(BaseModel):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    is_active = db.Column(db.Boolean, default=True)

class Booking(BaseModel):
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

class Order(BaseModel):
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

class OrderItem(BaseModel):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    pet_for_sale_id = db.Column(db.Integer, db.ForeignKey('pets_for_sale.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Price at time of order


