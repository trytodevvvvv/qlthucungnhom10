from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import services_bp
from app.models import PetService, ServiceCategory
from app.extensions import db

@services_bp.route('/services')
@login_required
def list_services():
    services = PetService.query.all()
    return render_template('services/services.html', services=services)

@services_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    categories = ServiceCategory.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        duration_minutes = request.form.get('duration_minutes')
        is_active = request.form.get('is_active') == 'on'
        
        try:
            price = float(price) if price else 0.0
            duration_minutes = int(duration_minutes) if duration_minutes else 30
            
            new_service = PetService(
                name=name, category_id=category_id, 
                price=price, duration_minutes=duration_minutes, is_active=is_active
            )
            db.session.add(new_service)
            db.session.commit()
            flash('Thêm dịch vụ thành công!', 'success')
            return redirect(url_for('services.list_services'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra.', 'danger')
            
    return render_template('services/service_form.html', service=None, categories=categories)

@services_bp.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = PetService.query.get_or_404(id)
    categories = ServiceCategory.query.all()
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.category_id = request.form.get('category_id')
        price = request.form.get('price')
        duration_minutes = request.form.get('duration_minutes')
        service.is_active = request.form.get('is_active') == 'on'
        
        try:
            service.price = float(price) if price else 0.0
            service.duration_minutes = int(duration_minutes) if duration_minutes else 30
            
            db.session.commit()
            flash('Cập nhật dịch vụ thành công!', 'success')
            return redirect(url_for('services.list_services'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra.', 'danger')
            
    return render_template('services/service_form.html', service=service, categories=categories)

@services_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    service = PetService.query.get_or_404(id)
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Đã xóa dịch vụ!', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Không thể xóa dịch vụ này do ràng buộc dữ liệu.', 'danger')
    return redirect(url_for('services.list_services'))
