from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Order, OrderItem, Product, PetService, Customer, Booking
from app.extensions import db
from datetime import datetime
from . import reports_bp

@reports_bp.route('/reports')
@login_required
def index():
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền xem báo cáo.', 'danger')
        return redirect(url_for('dashboard.index'))

    current_year = datetime.now().year
    
    # 1. Doanh thu theo tháng (năm hiện tại)
    monthly_sales_query = db.session.query(
        func.extract('month', Order.created_at).label('month'),
        func.sum(Order.total_amount).label('total')
    ).filter(
        func.extract('year', Order.created_at) == current_year,
        Order.status == 'Completed'
    ).group_by(
        func.extract('month', Order.created_at)
    ).all()

    monthly_sales = [0] * 12
    for item in monthly_sales_query:
        if item.month:
            monthly_sales[int(item.month) - 1] = float(item.total)

    # 2. Phân tích Lịch hẹn
    bookings_query = db.session.query(
        Booking.status,
        func.count(Booking.id)
    ).group_by(Booking.status).all()
    
    booking_stats = {
        'labels': [],
        'data': []
    }
    for status, count in bookings_query:
        booking_stats['labels'].append(status)
        booking_stats['data'].append(count)

    # 3. Top 5 Khách hàng chi tiêu cao nhất
    top_customers = Customer.query.order_by(Customer.total_spent.desc()).limit(5).all()

    # 4. Top 5 Sản phẩm bán chạy
    top_products_query = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_qty')
    ).join(OrderItem, Product.id == OrderItem.product_id)\
    .join(Order, OrderItem.order_id == Order.id)\
    .filter(Order.status == 'Completed')\
    .group_by(Product.id)\
    .order_by(func.sum(OrderItem.quantity).desc())\
    .limit(5).all()

    top_products = [{'name': name, 'qty': qty} for name, qty in top_products_query]

    # Tổng kết chung
    total_revenue_year = sum(monthly_sales)
    total_orders_year = Order.query.filter(func.extract('year', Order.created_at) == current_year, Order.status == 'Completed').count()
    total_customers = Customer.query.count()

    return render_template('reports/index.html',
                           current_year=current_year,
                           monthly_sales=monthly_sales,
                           booking_stats=booking_stats,
                           top_customers=top_customers,
                           top_products=top_products,
                           total_revenue_year=total_revenue_year,
                           total_orders_year=total_orders_year,
                           total_customers=total_customers)
