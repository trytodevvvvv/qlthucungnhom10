from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from . import bookings_bp
from app.models import Booking, Customer, Pet, PetService, User, Order, OrderItem, Voucher
from app.extensions import db

@bookings_bp.route('/bookings')
@login_required
def list_bookings():
    query = Booking.query
    
    # Phân quyền xem lịch hẹn
    if current_user.role == 'customer':
        # Khách hàng chỉ xem lịch của chính mình
        query = query.filter_by(customer_id=current_user.customer_id)
    elif current_user.role in ['staff', 'veterinarian', 'groomer']:
        # Nhân viên chuyên môn xem lịch được phân công cho mình
        query = query.filter_by(employee_id=current_user.id)
    # admin và receptionist xem được tất cả
    
    bookings = query.order_by(Booking.booking_time.asc()).all()
    return render_template('bookings/bookings.html', bookings=bookings)

@bookings_bp.route('/bookings/add', methods=['GET', 'POST'])
@login_required
def add_booking():
    customers = Customer.query.all()
    pets = Pet.query.all()
    services = PetService.query.all()
    employees = User.query.filter(User.role != 'customer').all()
    
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        pet_id = request.form.get('pet_id')
        service_id = request.form.get('service_id')
        employee_id = request.form.get('employee_id')
        booking_time_str = request.form.get('booking_time')
        notes = request.form.get('notes')
        is_paid = 'is_paid' in request.form
        
        try:
            booking_time = datetime.fromisoformat(booking_time_str) if booking_time_str else datetime.now()
            employee_id = employee_id if employee_id else None
            
            new_booking = Booking(
                customer_id=customer_id, pet_id=pet_id, service_id=service_id, 
                employee_id=employee_id, booking_time=booking_time, 
                status='Confirmed', notes=notes, is_paid=is_paid
            )
            db.session.add(new_booking)
            db.session.flush()

            # Nếu đã thanh toán, tạo hóa đơn POS
            if is_paid:
                service = PetService.query.get(service_id)
                if service:
                    new_order = Order(
                        customer_id=customer_id,
                        user_id=current_user.id,
                        total_amount=service.price,
                        payment_method='Banking', # Mặc định hoặc tùy chọn
                        status='Completed'
                    )
                    db.session.add(new_order)
                    db.session.flush()
                    
                    order_item = OrderItem(
                        order_id=new_order.id,
                        service_id=service_id,
                        quantity=1,
                        price=service.price
                    )
                    db.session.add(order_item)
                    
                    # Cập nhật hạng khách hàng
                    customer = Customer.query.get(customer_id)
                    if customer:
                        customer.update_tier()

            db.session.commit()
            flash('Thêm lịch hẹn thành công!', 'success')
            return redirect(url_for('bookings.list_bookings'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra: ' + str(e), 'danger')
            
    return render_template('bookings/booking_form.html', booking=None, customers=customers, pets=pets, services=services, employees=employees)

@bookings_bp.route('/bookings/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_booking(id):
    booking = Booking.query.get_or_404(id)
    customers = Customer.query.all()
    pets = Pet.query.all()
    services = PetService.query.all()
    employees = User.query.filter(User.role != 'customer').all()
    
    if request.method == 'POST':
        old_is_paid = booking.is_paid
        booking.customer_id = request.form.get('customer_id')
        booking.pet_id = request.form.get('pet_id')
        booking.service_id = request.form.get('service_id')
        employee_id = request.form.get('employee_id')
        booking.employee_id = employee_id if employee_id else None
        
        booking_time_str = request.form.get('booking_time')
        if booking_time_str:
            booking.booking_time = datetime.fromisoformat(booking_time_str)
            
        booking.is_paid = 'is_paid' in request.form
        booking.notes = request.form.get('notes')
        
        try:
            # Nếu vừa mới thanh toán xong (từ False sang True), tạo hóa đơn
            if booking.is_paid and not old_is_paid:
                service = PetService.query.get(booking.service_id)
                if service:
                    new_order = Order(
                        customer_id=booking.customer_id,
                        user_id=current_user.id,
                        total_amount=service.price,
                        payment_method='Banking',
                        status='Completed'
                    )
                    db.session.add(new_order)
                    db.session.flush()
                    
                    order_item = OrderItem(
                        order_id=new_order.id,
                        service_id=booking.service_id,
                        quantity=1,
                        price=service.price
                    )
                    db.session.add(order_item)
                    
                    # Cập nhật hạng khách hàng
                    customer = Customer.query.get(booking.customer_id)
                    if customer:
                        customer.update_tier()

            db.session.commit()
            flash('Cập nhật lịch hẹn thành công!', 'success')
            return redirect(url_for('bookings.list_bookings'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra: ' + str(e), 'danger')
            
    return render_template('bookings/booking_form.html', booking=booking, customers=customers, pets=pets, services=services, employees=employees)

@bookings_bp.route('/bookings/delete/<int:id>', methods=['POST'])
@login_required
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    try:
        db.session.delete(booking)
        db.session.commit()
        flash('Đã xóa lịch hẹn!', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Không thể xóa.', 'danger')
    return redirect(url_for('bookings.list_bookings'))

@bookings_bp.route('/bookings/pay/<int:id>', methods=['POST'])
@login_required
def pay_booking(id):
    booking = Booking.query.get_or_404(id)
    payment_method = request.form.get('payment_method', 'Cash')
    coupon_code = request.form.get('coupon_code')
    
    if booking.is_paid:
        flash('Lịch hẹn này đã được thanh toán rồi.', 'info')
        return redirect(url_for('bookings.list_bookings'))
        
    try:
        subtotal = booking.service.price
        discount = 0
        
        # Áp dụng mã giảm giá nếu có
        if coupon_code and booking.customer:
            voucher = Voucher.query.filter_by(code=coupon_code, is_active=True).first()
            customer = booking.customer
            if voucher:
                allowed_tiers = ['Gold', 'Platinum', 'Diamond', 'VIP']
                tier_priority = {'Standard': 0, 'Silver': 1, 'Gold': 2, 'Platinum': 3, 'Diamond': 4, 'VIP': 5}
                if customer.tier in allowed_tiers and tier_priority.get(customer.tier, 0) >= tier_priority.get(voucher.min_tier, 2):
                    if subtotal >= voucher.min_order_amount:
                        if voucher.discount_type == 'fixed':
                            discount = voucher.discount_amount
                        else:
                            discount = (voucher.discount_amount / 100) * subtotal
        
        total_amount = max(0, subtotal - discount)

        # 1. Tạo hóa đơn POS
        new_order = Order(
            customer_id=booking.customer_id,
            user_id=current_user.id,
            total_amount=total_amount,
            payment_method=payment_method,
            status='Completed'
        )
        db.session.add(new_order)
        db.session.flush()
        
        # 2. Tạo chi tiết hóa đơn
        order_item = OrderItem(
            order_id=new_order.id,
            service_id=booking.service_id,
            quantity=1,
            price=subtotal # Giá gốc
        )
        db.session.add(order_item)
        
        # 3. Cập nhật trạng thái lịch hẹn
        booking.is_paid = True
        
        # 4. Cập nhật hạng khách hàng
        if booking.customer:
            booking.customer.update_tier()
            
        db.session.commit()
        flash(f'Thanh toán thành công dịch vụ {booking.service.name}! (Giảm: {discount:,.0f}đ)', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Lỗi khi thanh toán: ' + str(e), 'danger')
        
    return redirect(url_for('bookings.list_bookings'))
