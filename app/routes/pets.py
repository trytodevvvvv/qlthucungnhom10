from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import pets_bp
from app.models import Customer, Pet, User
from app.extensions import db

@pets_bp.route('/customers')
@login_required
def list_customers():
    customers = Customer.query.all()
    return render_template('pets/customers.html', customers=customers)

@pets_bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        tier = request.form.get('tier', 'Standard')
        
        new_customer = Customer(name=name, phone=phone, address=address, tier=tier)
        db.session.add(new_customer)
        
        try:
            db.session.flush()
            
            # Tự động tạo tài khoản đăng nhập cho khách hàng
            # Username = SĐT, mật khẩu mặc định = 123456
            username = phone
            default_password = '123456'
            
            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    role='customer',
                    full_name=name,
                    phone=phone,
                    customer_id=new_customer.id,
                    plain_password=default_password
                )
                user.set_password(default_password)
                db.session.add(user)
            
            db.session.commit()
            flash('Thêm khách hàng thành công! Tài khoản đăng nhập đã được tạo tự động.', 'success')
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
        customer.tier = request.form.get('tier')
        
        # Đồng bộ thông tin sang tài khoản user nếu có
        if customer.user_account:
            customer.user_account.full_name = customer.name
            email = request.form.get('email')
            if email:
                customer.user_account.email = email
        
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
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Đã xóa khách hàng!', 'info')
    return redirect(url_for('pets.list_customers'))

@pets_bp.route('/pets')
@login_required
def list_pets():
    query = Pet.query
    if current_user.role == 'customer':
        query = query.filter_by(customer_id=current_user.customer_id)
    
    pets = query.all()
    return render_template('pets/pets.html', pets=pets)

@pets_bp.route('/pets/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    customers = Customer.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        weight = request.form.get('weight')
        customer_id = request.form.get('customer_id')
        health_notes = request.form.get('health_notes')
        
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
        pet.name = request.form.get('name')
        pet.species = request.form.get('species')
        pet.breed = request.form.get('breed')
        weight = request.form.get('weight')
        pet.customer_id = request.form.get('customer_id')
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
