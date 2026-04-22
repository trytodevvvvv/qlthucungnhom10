from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import json
from . import pos_bp
from app.models import Product, PetService, Customer, Order, OrderItem
from app.extensions import db

@pos_bp.route('/pos')
@login_required
def index():
    products = Product.query.filter(Product.stock_quantity > 0).all()
    services = PetService.query.filter_by(is_active=True).all()
    customers = Customer.query.all()
    return render_template('pos/index.html', products=products, services=services, customers=customers)

@pos_bp.route('/pos/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        # Nhận dữ liệu giỏ hàng dưới dạng JSON từ form ẩn
        cart_data_raw = request.form.get('cart_data')
        customer_id = request.form.get('customer_id')
        payment_method = request.form.get('payment_method', 'Cash')
        
        if not cart_data_raw:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        cart_items = json.loads(cart_data_raw)
        if len(cart_items) == 0:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        total_amount = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
        
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
        flash(f'Thanh toán thành công! Mã hóa đơn: #{new_order.id}', 'success')
        return redirect(url_for('pos.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi thanh toán: {str(e)}', 'danger')
        return redirect(url_for('pos.index'))
