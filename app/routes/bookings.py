from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from . import bookings_bp
from app.models import Booking, Customer, Pet, PetService, User
from app.extensions import db

@bookings_bp.route('/bookings')
@login_required
def list_bookings():
    bookings = Booking.query.order_by(Booking.booking_time.asc()).all()
    return render_template('bookings/bookings.html', bookings=bookings)

@bookings_bp.route('/bookings/add', methods=['GET', 'POST'])
@login_required
def add_booking():
    customers = Customer.query.all()
    pets = Pet.query.all()
    services = PetService.query.all()
    employees = User.query.filter(User.role != 'customer').all() # usually all grooming staff
    
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        pet_id = request.form.get('pet_id')
        service_id = request.form.get('service_id')
        employee_id = request.form.get('employee_id')
        booking_time_str = request.form.get('booking_time')
        status = request.form.get('status', 'Pending')
        notes = request.form.get('notes')
        
        try:
            booking_time = datetime.fromisoformat(booking_time_str) if booking_time_str else datetime.utcnow()
            employee_id = employee_id if employee_id else None
            
            new_booking = Booking(
                customer_id=customer_id, pet_id=pet_id, service_id=service_id, 
                employee_id=employee_id, booking_time=booking_time, 
                status=status, notes=notes
            )
            db.session.add(new_booking)
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
        booking.customer_id = request.form.get('customer_id')
        booking.pet_id = request.form.get('pet_id')
        booking.service_id = request.form.get('service_id')
        employee_id = request.form.get('employee_id')
        booking.employee_id = employee_id if employee_id else None
        
        booking_time_str = request.form.get('booking_time')
        if booking_time_str:
            booking.booking_time = datetime.fromisoformat(booking_time_str)
            
        booking.status = request.form.get('status')
        booking.notes = request.form.get('notes')
        
        try:
            db.session.commit()
            flash('Cập nhật lịch hẹn thành công!', 'success')
            return redirect(url_for('bookings.list_bookings'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra.', 'danger')
            
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
