from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import json
from . import pos_bp
from app.models import Product, PetService, Customer, Order, OrderItem, Voucher
from app.extensions import db

from datetime import datetime

@pos_bp.route('/pos')
@login_required
def index():
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền truy cập vào chức năng bán hàng!', 'danger')
        return redirect(url_for('dashboard.index'))
    products = Product.query.filter(Product.stock_quantity > 0).all()
    services = PetService.query.filter_by(is_active=True).all()
    customers = Customer.query.all()
    
    # Lấy các tham số lọc
    search_id = request.args.get('search_id')
    customer_name = request.args.get('customer_name')
    payment_method = request.args.get('payment_method')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Query cơ bản cho Order
    query = Order.query

    # Áp dụng các bộ lọc
    if search_id:
        query = query.filter(Order.id == search_id)
    if customer_name:
        query = query.join(Customer).filter(Customer.name.ilike(f'%{customer_name}%'))
    if payment_method:
        query = query.filter(Order.payment_method == payment_method)
    if min_price is not None:
        query = query.filter(Order.total_amount >= min_price)
    if max_price is not None:
        query = query.filter(Order.total_amount <= max_price)
    if start_date:
        query = query.filter(Order.created_at >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        # Thêm 23:59:59 để bao gồm cả ngày kết thúc
        query = query.filter(Order.created_at <= datetime.strptime(f"{end_date} 23:59:59", '%Y-%m-%d %H:%M:%S'))

    # Phân trang
    page = request.args.get('page', 1, type=int)
    per_page = 10
    orders_pagination = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    recent_orders = orders_pagination.items
    
    # Tính tổng doanh thu hệ thống (dựa trên kết quả đã lọc)
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    return render_template('pos/index.html', 
                           products=products, 
                           services=services, 
                           customers=customers,
                           recent_orders=recent_orders,
                           orders_pagination=orders_pagination,
                           total_revenue=total_revenue,
                           filters=request.args)

@pos_bp.route('/pos/apply_voucher', methods=['POST'])
@login_required
def apply_voucher():
    data = request.get_json()
    code = data.get('code')
    customer_id = data.get('customer_id')
    order_amount = data.get('order_amount', 0)
    
    voucher = Voucher.query.filter_by(code=code, is_active=True).first()
    if not voucher:
        return jsonify({'success': False, 'message': 'Mã giảm giá không hợp lệ hoặc đã hết hạn.'})
    
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'success': False, 'message': 'Không tìm thấy thông tin khách hàng.'})
    
    # Kiểm tra hạng (Gold, Platinum, Diamond, VIP mới được dùng)
    allowed_tiers = ['Gold', 'Platinum', 'Diamond', 'VIP']
    if customer.tier not in allowed_tiers:
        return jsonify({'success': False, 'message': f'Mã giảm giá này chỉ dành cho hạng Vàng trở lên. Hạng hiện tại: {customer.tier}'})
    
    # Kiểm tra hạng tối thiểu của voucher
    tier_priority = {'Standard': 0, 'Silver': 1, 'Gold': 2, 'Platinum': 3, 'Diamond': 4, 'VIP': 5}
    if tier_priority.get(customer.tier, 0) < tier_priority.get(voucher.min_tier, 2):
        return jsonify({'success': False, 'message': f'Hạng của bạn ({customer.tier}) chưa đủ để dùng mã này (Yêu cầu: {voucher.min_tier})'})

    if order_amount < voucher.min_order_amount:
        return jsonify({'success': False, 'message': f'Đơn hàng tối thiểu {voucher.min_order_amount:,.0f}đ để dùng mã này.'})
        
    discount = 0
    if voucher.discount_type == 'fixed':
        discount = voucher.discount_amount
    else:
        discount = (voucher.discount_amount / 100) * order_amount
        
    return jsonify({
        'success': True, 
        'discount_amount': discount,
        'discount_percent': voucher.discount_amount if voucher.discount_type == 'percentage' else None,
        'message': 'Áp dụng mã giảm giá thành công!'
    })

@pos_bp.route('/pos/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        # Nhận dữ liệu giỏ hàng dưới dạng JSON từ form ẩn
        cart_data_raw = request.form.get('cart_data')
        customer_id_raw = request.form.get('customer_id')
        customer_id = int(customer_id_raw) if customer_id_raw and customer_id_raw.strip() else None
        payment_method = request.form.get('payment_method', 'Cash')
        coupon_code = request.form.get('coupon_code')
        
        if not cart_data_raw:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        cart_items = json.loads(cart_data_raw)
        if len(cart_items) == 0:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        subtotal = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
        discount = 0
        
        # Áp dụng voucher nếu có
        if coupon_code and customer_id:
            voucher = Voucher.query.filter_by(code=coupon_code, is_active=True).first()
            customer = Customer.query.get(customer_id)
            if voucher and customer:
                # Re-validate logic for security
                allowed_tiers = ['Gold', 'Platinum', 'Diamond', 'VIP']
                tier_priority = {'Standard': 0, 'Silver': 1, 'Gold': 2, 'Platinum': 3, 'Diamond': 4, 'VIP': 5}
                if customer.tier in allowed_tiers and tier_priority.get(customer.tier, 0) >= tier_priority.get(voucher.min_tier, 2):
                    if subtotal >= voucher.min_order_amount:
                        if voucher.discount_type == 'fixed':
                            discount = voucher.discount_amount
                        else:
                            discount = (voucher.discount_amount / 100) * subtotal
        
        total_amount = max(0, subtotal - discount)
        
        # Tạo Order
        new_order = Order(
            customer_id=customer_id if customer_id else None,
            user_id=current_user.id,
            total_amount=total_amount,
            payment_method=payment_method,
            status='Completed'
        )
        db.session.add(new_order)
        db.session.flush() # Lấy order.id
        
        # Tạo Order Items
        for item in cart_items:
            product_id = item['id'] if item['type'] == 'product' else None
            service_id = item['id'] if item['type'] == 'service' else None
            
            # Trừ kho nếu là sản phẩm
            if product_id:
                product = Product.query.get(product_id)
                if product:
                    product.stock_quantity = max(0, product.stock_quantity - int(item['quantity']))
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product_id,
                service_id=service_id,
                quantity=int(item['quantity']),
                price=float(item['price'])
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        # Cập nhật hạng khách hàng
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                customer.update_tier()
        
        flash(f'Thanh toán thành công! Mã hóa đơn: #{new_order.id}', 'success')
        return redirect(url_for('pos.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi thanh toán: {str(e)}', 'danger')
        return redirect(url_for('pos.index'))
