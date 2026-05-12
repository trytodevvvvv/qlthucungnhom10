from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import PetForSale, Product, Customer, Order, OrderItem, Pet
from app.extensions import db
from datetime import datetime
from . import pet_sales_bp

@pet_sales_bp.route('/pet-sales')
@login_required
def index():
    pets = PetForSale.query.filter_by(status='Available').all()
    return render_template('pet_sales/index.html', pets=pets)

@pet_sales_bp.route('/pet-sales/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền thêm thú cưng bán.', 'danger')
        return redirect(url_for('pet_sales.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        price = request.form.get('price')
        quantity = request.form.get('quantity', 1)
        health_notes = request.form.get('health_notes')
        
        pet = PetForSale(
            name=name,
            species=species,
            breed=breed,
            age=age,
            price=float(price),
            quantity=int(quantity),
            health_notes=health_notes
        )
        db.session.add(pet)
        db.session.commit()
        flash('Thêm thú cưng bán thành công!', 'success')
        return redirect(url_for('inventory.list_products'))
        
    return render_template('pet_sales/form.html', pet=None)

@pet_sales_bp.route('/pet-sales/edit/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền sửa thú cưng bán.', 'danger')
        return redirect(url_for('inventory.list_products'))

    pet = PetForSale.query.get_or_404(pet_id)
    if request.method == 'POST':
        pet.name         = request.form.get('name')
        pet.species      = request.form.get('species')
        pet.breed        = request.form.get('breed')
        pet.age          = request.form.get('age')
        pet.price        = float(request.form.get('price'))
        new_qty          = int(request.form.get('quantity', 0))
        pet.quantity     = max(0, new_qty)
        pet.health_notes = request.form.get('health_notes')

        # Tự động cập nhật trạng thái theo số lượng
        if pet.quantity > 0:
            pet.status = 'Available'   # Có hàng → hiện trên trang bán
        else:
            pet.status = 'Sold'        # Hết hàng → ẩn khỏi trang bán

        db.session.commit()
        status_label = 'sẵn hàng' if pet.quantity > 0 else 'hết hàng'
        flash(f'Cập nhật thú cưng thành công! Trạng thái: {status_label} ({pet.quantity} con).', 'success')
        return redirect(url_for('inventory.list_products'))
        
    return render_template('pet_sales/form.html', pet=pet)

@pet_sales_bp.route('/pet-sales/delete/<int:pet_id>', methods=['POST'])
@login_required
def delete_pet(pet_id):
    if current_user.role not in ['admin']:
        flash('Chỉ quản trị viên mới được xóa thú cưng bán.', 'danger')
        return redirect(url_for('inventory.list_products'))

    pet = PetForSale.query.get_or_404(pet_id)
    try:
        db.session.delete(pet)
        db.session.commit()
        flash('Đã xóa thú cưng thành công!', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Không thể xóa thú cưng do ràng buộc dữ liệu.', 'danger')
        
    return redirect(url_for('inventory.list_products'))

@pet_sales_bp.route('/pet-sales/checkout/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def checkout(pet_id):
    if current_user.role not in ['admin', 'receptionist']:
        flash('Bạn không có quyền thực hiện bán thú cưng.', 'danger')
        return redirect(url_for('pet_sales.index'))

    pet_for_sale = PetForSale.query.get_or_404(pet_id)
    if pet_for_sale.status != 'Available':
        flash('Thú cưng này đã được bán.', 'warning')
        return redirect(url_for('pet_sales.index'))
        
    products = Product.query.filter(Product.stock_quantity > 0).all()
    customers = Customer.query.all()
    
    if request.method == 'POST':
        payment_method      = request.form.get('payment_method', 'Cash')
        customer_mode       = request.form.get('customer_mode', 'existing')
        pet_qty             = int(request.form.get('pet_quantity', 1))
        customer_id         = None

        # ── Khách hàng mới ──────────────────────────────────────────
        if customer_mode == 'new':
            new_name  = request.form.get('new_cust_name', '').strip()
            new_phone = request.form.get('new_cust_phone', '').strip()

            if not new_name:
                flash('Vui lòng nhập tên khách hàng mới.', 'danger')
                return redirect(url_for('pet_sales.checkout', pet_id=pet_id))

            # Nếu có SĐT, kiểm tra xem đã tồn tại chưa
            if new_phone:
                cust = Customer.query.filter_by(phone=new_phone).first()
                if cust:
                    # Nếu tồn tại rồi thì dùng luôn khách cũ (Seamless link)
                    customer_id = cust.id
                else:
                    # Tạo mới hoàn toàn
                    new_cust = Customer(name=new_name, phone=new_phone)
                    db.session.add(new_cust)
                    db.session.flush()
                    customer_id = new_cust.id
            else:
                # Không có SĐT → Báo lỗi vì DB yêu cầu phone nullable=False
                flash('Số điện thoại là bắt buộc để lưu thông tin khách hàng mới.', 'warning')
                return redirect(url_for('pet_sales.checkout', pet_id=pet_id))

        # ── Khách có sẵn (datalist "SĐT - Tên") ────────────────────
        else:
            customer_identifier = request.form.get('customer_identifier', '').strip()
            if not customer_identifier:
                flash('Vui lòng chọn hoặc nhập thông tin khách hàng.', 'danger')
                return redirect(url_for('pet_sales.checkout', pet_id=pet_id))

            # Parse "SĐT - Tên"
            if ' - ' in customer_identifier:
                phone_part = customer_identifier.split(' - ')[0].strip()
                cust = Customer.query.filter_by(phone=phone_part).first()
                if cust:
                    customer_id = cust.id

            # Fallback tìm theo tên
            if not customer_id:
                name_part = customer_identifier.split(' - ')[-1].strip()
                cust = Customer.query.filter(Customer.name.ilike(f'%{name_part}%')).first()
                if cust:
                    customer_id = cust.id

            # Vẫn không tìm thấy → Đây là trường hợp gõ tên lạ vào ô search
            if not customer_id:
                # Vì phone là bắt buộc, ta không thể tạo customer chỉ với name ở đây.
                # Yêu cầu người dùng sang tab "Khách mới" để nhập đầy đủ.
                flash('Khách hàng không tồn tại. Vui lòng sử dụng tab "Khách mới" để nhập đầy đủ Tên và SĐT.', 'warning')
                return redirect(url_for('pet_sales.checkout', pet_id=pet_id))

        # Validate số lượng mua
        if pet_qty < 1 or pet_qty > pet_for_sale.quantity:
            flash(f'Số lượng không hợp lệ. Còn lại: {pet_for_sale.quantity} con.', 'danger')
            return redirect(url_for('pet_sales.checkout', pet_id=pet_id))

        product_ids = request.form.getlist('product_id[]')
        quantities  = request.form.getlist('quantity[]')

        total_amount = pet_for_sale.price * pet_qty

        # Tạo Order
        new_order = Order(
            customer_id=customer_id,
            user_id=current_user.id,
            total_amount=0,  # Sẽ cập nhật sau
            payment_method=payment_method,
            status='Completed'
        )
        db.session.add(new_order)
        db.session.flush()

        # Thêm thú cưng vào OrderItem (với số lượng đã chọn)
        pet_item = OrderItem(
            order_id=new_order.id,
            pet_for_sale_id=pet_id,
            quantity=pet_qty,
            price=pet_for_sale.price
        )
        db.session.add(pet_item)

        # Thêm các sản phẩm vào OrderItem
        for p_id, qty in zip(product_ids, quantities):
            if p_id and int(qty) > 0:
                prod = Product.query.get(p_id)
                if prod and prod.stock_quantity >= int(qty):
                    prod.stock_quantity -= int(qty)
                    total_amount += prod.price * int(qty)
                    item = OrderItem(
                        order_id=new_order.id,
                        product_id=p_id,
                        quantity=int(qty),
                        price=prod.price
                    )
                    db.session.add(item)

        new_order.total_amount = total_amount

        # Trừ số lượng thú cưng trong kho
        pet_for_sale.quantity -= pet_qty
        if pet_for_sale.quantity <= 0:
            pet_for_sale.status = 'Sold'
            pet_for_sale.quantity = 0

        # Tự động tạo hồ sơ thú cưng cho khách hàng (chỉ khi có customer_id)
        if customer_id:
            for i in range(pet_qty):
                suffix = f' #{i+1}' if pet_qty > 1 else ''
                new_customer_pet = Pet(
                    customer_id=customer_id,
                    name=pet_for_sale.name + suffix,
                    species=pet_for_sale.species,
                    breed=pet_for_sale.breed,
                    health_notes=f"Mua từ cửa hàng (Mã ĐH: #{new_order.id}). {pet_for_sale.health_notes or ''}",
                    source='store_purchase',
                    purchase_order_id=new_order.id
                )
                db.session.add(new_customer_pet)

        try:
            db.session.commit()
            customer = Customer.query.get(customer_id)
            if customer:
                customer.update_total_spent()

            flash(f'Bán {pet_qty} thú cưng thành công! Đơn hàng: #{new_order.id}. Đã tạo hồ sơ thú cưng cho khách.', 'success')
            return redirect(url_for('pet_sales.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi khi thanh toán: {str(e)}', 'danger')
            return redirect(url_for('pet_sales.checkout', pet_id=pet_id))
            
    return render_template('pet_sales/checkout.html', pet=pet_for_sale, products=products, customers=customers)
