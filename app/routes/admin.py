from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps
from . import admin_bp
from app.models import User, Customer
from app.extensions import db

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Bạn không có quyền truy cập vào chức năng này!', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/users')
@login_required
@admin_required
def list_users():
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    
    query = User.query
    
    if search:
        query = query.filter(db.or_(
            User.username.ilike(f'%{search}%'),
            User.full_name.ilike(f'%{search}%'),
            User.phone.ilike(f'%{search}%')
        ))
        
    if role_filter:
        query = query.filter_by(role=role_filter)
        
    if status_filter:
        is_active = status_filter == '1'
        query = query.filter_by(is_active=is_active)
        
    users = query.all()
    
    filters = {
        'search': search,
        'role': role_filter,
        'status': status_filter
    }
    
    return render_template('admin/users.html', users=users, filters=filters)

@admin_bp.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        email = request.form.get('email') or None
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'danger')
            return render_template('admin/user_form.html')
        
        phone = request.form.get('phone')
        
        user = User(
            username=username,
            role=role,
            full_name=full_name,
            email=email,
            phone=phone,
            plain_password=password
        )
        user.set_password(password)
        
        # Nếu là khách hàng, tự động tạo hồ sơ Customer
        if role == 'customer':
            address = request.form.get('address')
            tier = request.form.get('tier', 'Standard')
            
            if not phone:
                flash('Số điện thoại là bắt buộc cho tài khoản khách hàng!', 'danger')
                return render_template('admin/user_form.html')
            
            # Kiểm tra SĐT đã tồn tại chưa
            existing = Customer.query.filter_by(phone=phone).first()
            if existing:
                flash('Số điện thoại này đã được đăng ký cho khách hàng khác!', 'danger')
                return render_template('admin/user_form.html')
            
            customer = Customer(
                name=full_name or username,
                phone=phone,
                address=address,
                tier=tier
            )
            db.session.add(customer)
            db.session.flush()  # Lấy customer.id
            user.customer_id = customer.id
        
        db.session.add(user)
        db.session.commit()
        flash('Tạo tài khoản thành công!', 'success')
        return redirect(url_for('admin.list_users'))
            
    return render_template('admin/user_form.html')

@admin_bp.route('/admin/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        # Không cho phép sửa quyền hạn của tài khoản 'admin' gốc
        if user.username == 'admin':
            user.role = 'admin'
            user.is_active = True
        else:
            user.role = request.form.get('role')
            user.is_active = 'is_active' in request.form
            
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email') or None
        user.phone = request.form.get('phone')
        
        # Cập nhật thông tin khách hàng nếu là customer
        if user.role == 'customer':
            phone = user.phone
            address = request.form.get('address')
            tier = request.form.get('tier', 'Standard')
            
            if not phone:
                flash('Số điện thoại là bắt buộc cho tài khoản khách hàng!', 'danger')
                return render_template('admin/user_form.html', user=user)
            
            if user.customer_profile:
                # Cập nhật hồ sơ khách hàng đã có
                user.customer_profile.name = user.full_name or user.username
                user.customer_profile.phone = phone
                user.customer_profile.address = address
                user.customer_profile.tier = tier
            else:
                # Tạo hồ sơ khách hàng mới
                existing = Customer.query.filter_by(phone=phone).first()
                if existing:
                    flash('Số điện thoại này đã được đăng ký cho khách hàng khác!', 'danger')
                    return render_template('admin/user_form.html', user=user)
                    
                customer = Customer(
                    name=user.full_name or user.username,
                    phone=phone,
                    address=address,
                    tier=tier
                )
                db.session.add(customer)
                db.session.flush()
                user.customer_id = customer.id
            
        password = request.form.get('password')
        if password:
            user.set_password(password)
            user.plain_password = password
            
        try:
            db.session.commit()
            flash('Cập nhật tài khoản thành công!', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception:
            db.session.rollback()
            flash('Lỗi khi cập nhật tài khoản!', 'danger')
        
    return render_template('admin/user_form.html', user=user)

@admin_bp.route('/admin/user/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Bạn không thể xóa chính mình!', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'Kích hoạt' if user.is_active else 'Vô hiệu hóa'
        flash(f'Đã {status} tài khoản!', 'success')
    return redirect(url_for('admin.list_users'))
