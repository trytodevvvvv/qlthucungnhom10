from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import json
from . import pos_bp
from app.models import Product, PetService, Customer, Order, OrderItem
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
    from app.models import PetForSale
    pets_for_sale = PetForSale.query.filter(PetForSale.status == 'Available', PetForSale.quantity > 0).all()
    customers = Customer.query.all()
    booking_id = request.args.get('booking_id')
    prefill_cart = []
    prefill_customer_identifier = ""
    if booking_id:
        from app.models import Booking
        booking = Booking.query.get(booking_id)
        if booking and not booking.is_paid:
            if booking.customer:
                prefill_customer_identifier = f"{booking.customer.phone} - {booking.customer.name}"
            if booking.service:
                prefill_cart.append({
                    'type': 'service',
                    'id': booking.service.id,
                    'name': f"{booking.service.name} (Lịch hẹn #{booking.id})",
                    'price': booking.service.price,
                    'quantity': 1,
                    'booking_id': booking.id
                })

    return render_template('pos/index.html', 
                           products=products, 
                           services=services, 
                           pets_for_sale=pets_for_sale,
                           customers=customers,
                           prefill_cart=prefill_cart,
                           prefill_customer_identifier=prefill_customer_identifier)

@pos_bp.route('/invoices')
@login_required
def list_invoices():
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền truy cập vào chức năng hóa đơn!', 'danger')
        return redirect(url_for('dashboard.index'))
    
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
    
    return render_template('pos/invoices.html', 
                           recent_orders=recent_orders,
                           orders_pagination=orders_pagination,
                           total_revenue=total_revenue,
                           filters=request.args)

@pos_bp.route('/pos/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        # Nhận dữ liệu giỏ hàng dưới dạng JSON từ form ẩn
        cart_data_raw = request.form.get('cart_data')
        customer_identifier = request.form.get('customer_identifier')
        customer_id = None
        
        if customer_identifier and ' - ' in customer_identifier:
            phone = customer_identifier.split(' - ')[0].strip()
            customer = Customer.query.filter_by(phone=phone).first()
            if customer:
                customer_id = customer.id

        payment_method = request.form.get('payment_method', 'Cash')
        
        if not cart_data_raw:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        cart_items = json.loads(cart_data_raw)
        if len(cart_items) == 0:
            flash('Giỏ hàng trống!', 'danger')
            return redirect(url_for('pos.index'))
            
        subtotal = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
        
        total_amount = max(0, subtotal)
        
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
        
        booking_ids_to_update = set()
        
        # Tạo Order Items
        for item in cart_items:
            product_id = item['id'] if item['type'] == 'product' else None
            service_id = item['id'] if item['type'] == 'service' else None
            pet_sale_id = item['id'] if item['type'] == 'pet' else None
            
            if 'booking_id' in item and item['booking_id']:
                booking_ids_to_update.add(item['booking_id'])
            
            # Trừ kho nếu là sản phẩm
            if product_id:
                product = Product.query.get(product_id)
                if product:
                    product.stock_quantity = max(0, product.stock_quantity - int(item['quantity']))

            # Xử lý thú cưng cần bán
            if pet_sale_id:
                from app.models import PetForSale, Pet
                pet_sale = PetForSale.query.get(pet_sale_id)
                qty_bought = int(item['quantity'])
                if pet_sale and pet_sale.quantity > 0:
                    pet_sale.quantity = max(0, pet_sale.quantity - qty_bought)
                    if pet_sale.quantity <= 0:
                        pet_sale.status = 'Sold'
                    
                    # Tự động tạo hồ sơ thú cưng cho khách hàng nếu có
                    if customer_id:
                        for i in range(qty_bought):
                            suffix = f' #{i+1}' if qty_bought > 1 else ''
                            new_customer_pet = Pet(
                                customer_id=customer_id,
                                name=pet_sale.name + suffix,
                                species=pet_sale.species,
                                breed=pet_sale.breed,
                                health_notes=f"Mua từ cửa hàng (Mã ĐH: #{new_order.id}). {pet_sale.health_notes or ''}",
                                source='store_purchase',
                                purchase_order_id=new_order.id
                            )
                            db.session.add(new_customer_pet)
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product_id,
                service_id=service_id,
                pet_for_sale_id=pet_sale_id,
                quantity=int(item['quantity']),
                price=float(item['price'])
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        if booking_ids_to_update:
            from app.models import Booking
            for b_id in booking_ids_to_update:
                booking = Booking.query.get(b_id)
                if booking:
                    booking.is_paid = True
            db.session.commit()
        
        # Cập nhật tổng chi tiêu khách hàng
        if customer_id:
            customer = Customer.query.get(customer_id)
            if customer:
                customer.update_total_spent()
        
        flash(f'Thanh toán thành công! Mã hóa đơn: #{new_order.id}', 'success')
        return redirect(url_for('pos.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi thanh toán: {str(e)}', 'danger')
        return redirect(url_for('pos.index'))

@pos_bp.route('/invoices/delete/<int:id>', methods=['POST'])
@login_required
def delete_invoice(id):
    if current_user.role != 'admin':
        flash('Chỉ Admin mới có quyền xóa hóa đơn!', 'danger')
        return redirect(url_for('pos.list_invoices'))
    
    order = Order.query.get_or_404(id)
    try:
        # Xóa các item liên quan (đã có cascade delete trong model nếu config đúng, nhưng ta cứ xóa cho chắc hoặc để SQLAlchemy lo)
        # Trong models.py: items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan') -> Nên nó tự xóa.
        db.session.delete(order)
        db.session.commit()
        flash(f'Đã xóa hóa đơn #{id} thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Lỗi khi xóa hóa đơn: {str(e)}', 'danger')
        
    return redirect(url_for('pos.list_invoices'))
