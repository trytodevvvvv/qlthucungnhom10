from flask import render_template
from flask_login import login_required
from app.models import Order, Customer, Pet, Booking, Product
from app.extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta
from . import dashboard_bp

@dashboard_bp.route('/')
@login_required
def index():
    # Basic Counts
    customer_count = Customer.query.count()
    pet_count = Pet.query.count()
    pending_bookings = Booking.query.filter_by(status='Pending').count()
    
    # Revenue Calculations
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    
    # Monthly Revenue
    first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_revenue = db.session.query(func.sum(Order.total_amount)).filter(Order.created_at >= first_day_of_month).scalar() or 0
    
    # Recent activity
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    upcoming_bookings = Booking.query.filter(Booking.status.in_(['Pending', 'Confirmed'])).order_by(Booking.booking_time.asc()).limit(5).all()
    
    # Low stock alerts
    low_stock_products = Product.query.filter(Product.stock_quantity <= 5).all()
    
    return render_template('dashboard/index.html', 
                           customer_count=customer_count,
                           pet_count=pet_count,
                           pending_bookings=pending_bookings,
                           total_revenue=total_revenue,
                           monthly_revenue=monthly_revenue,
                           recent_orders=recent_orders,
                           upcoming_bookings=upcoming_bookings,
                           low_stock_products=low_stock_products,
                           now=datetime.utcnow())
