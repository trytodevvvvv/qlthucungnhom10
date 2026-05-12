from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import pets_bp
from app.models import Customer, Pet, User
from app.extensions import db
from sqlalchemy import func
from flask import jsonify

@pets_bp.route('/customers')
@login_required
def list_customers():
    customers = Customer.query.all()
    
    # Đếm số thú cưng theo source cho từng khách hàng
    customer_pet_counts = {}
    for c in customers:
        owned_count = Pet.query.filter_by(customer_id=c.id, source='customer_owned').count()
        purchased_count = Pet.query.filter_by(customer_id=c.id, source='store_purchase').count()
        customer_pet_counts[c.id] = {
            'owned': owned_count,
            'purchased': purchased_count
        }
    
    return render_template('pets/customers.html', customers=customers, pet_counts=customer_pet_counts)

@pets_bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        new_customer = Customer(name=name, phone=phone, address=address)
        db.session.add(new_customer)
        
        try:
            db.session.commit()
            flash('Thêm khách hàng thành công!', 'success')
            return redirect(url_for('pets.list_customers'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra hoặc SĐT đã tồn tại.', 'danger')
            
    return render_template('pets/customer_form.html', customer=None)

@pets_bp.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        
        
        try:
            db.session.commit()
            flash('Cập nhật khách hàng thành công!', 'success')
            return redirect(url_for('pets.list_customers'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra hoặc SĐT trùng lặp.', 'danger')
            
    return render_template('pets/customer_form.html', customer=customer)

@pets_bp.route('/customers/delete/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    if current_user.role != 'admin':
        flash('Chỉ Admin mới có quyền xóa khách hàng!', 'danger')
        return redirect(url_for('pets.list_customers'))
        
    customer = Customer.query.get_or_404(id)
    try:
        # Gán customer_id trong các Order về NULL để tránh lỗi FK
        from app.models import Order, Booking
        Order.query.filter_by(customer_id=id).update({Order.customer_id: None})
        # Tương tự với Booking (hoặc xóa luôn booking nếu muốn, ở đây ta gán NULL nếu cho phép, hoặc xóa)
        # Booking thường đi kèm Pet, mà Pet sẽ bị xóa (cascade). Nên Booking cũng nên bị xóa.
        Booking.query.filter_by(customer_id=id).delete()
        
        db.session.delete(customer)
        db.session.commit()
        flash(f'Đã xóa khách hàng {customer.name} và các thú cưng liên quan!', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi xóa khách hàng: {str(e)}', 'danger')
        
    return redirect(url_for('pets.list_customers'))

@pets_bp.route('/pets')
@login_required
def list_pets():
    customer_id = request.args.get('customer_id')
    source = request.args.get('source', 'customer_owned')  # Mặc định: thú cưng khách hàng
    
    query = Pet.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    
    # Filter theo source
    if source in ['customer_owned', 'store_purchase']:
        query = query.filter_by(source=source)
    
    pets = query.all()
    return render_template('pets/pets.html', pets=pets, current_source=source)

@pets_bp.route('/pets/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    customers = Customer.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        weight = request.form.get('weight')
        customer_identifier = request.form.get('customer_identifier')
        health_notes = request.form.get('health_notes')
        
        # Extract phone from identifier "0912345678 - Nguyễn Văn A" or just "0912345678"
        phone = customer_identifier.split(' - ')[0].strip() if customer_identifier else ''
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            flash('Không tìm thấy khách hàng với số điện thoại này!', 'danger')
            return redirect(request.url)
            
        customer_id = customer.id
        
        # Parse weight
        try:
            weight = float(weight) if weight else None
        except:
            weight = None

        new_pet = Pet(
            name=name, species=species, breed=breed, 
            weight=weight, customer_id=customer_id, health_notes=health_notes
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('Thêm thú cưng thành công!', 'success')
        return redirect(url_for('pets.list_pets'))
        
    return render_template('pets/pet_form.html', pet=None, customers=customers)

@pets_bp.route('/pets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pet(id):
    pet = Pet.query.get_or_404(id)
    customers = Customer.query.all()
    if request.method == 'POST':
        customer_identifier = request.form.get('customer_identifier')
        phone = customer_identifier.split(' - ')[0].strip() if customer_identifier else ''
        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            flash('Không tìm thấy khách hàng với số điện thoại này!', 'danger')
            return redirect(request.url)

        pet.name = request.form.get('name')
        pet.species = request.form.get('species')
        pet.breed = request.form.get('breed')
        weight = request.form.get('weight')
        pet.customer_id = customer.id
        pet.health_notes = request.form.get('health_notes')
        
        try:
            pet.weight = float(weight) if weight else None
        except:
            pass

        db.session.commit()
        flash('Cập nhật thú cưng thành công!', 'success')
        return redirect(url_for('pets.list_pets'))
        
    return render_template('pets/pet_form.html', pet=pet, customers=customers)

@pets_bp.route('/pets/delete/<int:id>', methods=['POST'])
@login_required
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    flash('Đã xóa thú cưng!', 'info')
    return redirect(url_for('pets.list_pets'))

@pets_bp.route('/api/pets_by_customer')
@login_required
def api_pets_by_customer():
    phone = request.args.get('phone')
    if not phone:
        return jsonify([])
    
    customer = Customer.query.filter_by(phone=phone).first()
    if not customer:
        return jsonify([])
        
    pets = Pet.query.filter_by(customer_id=customer.id).all()
    pet_names = [p.name for p in pets]
    return jsonify(pet_names)
