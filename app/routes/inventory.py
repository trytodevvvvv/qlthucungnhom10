from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import inventory_bp
from app.models import Product, Category
from app.extensions import db

@inventory_bp.route('/products')
@login_required
def list_products():
    if current_user.role != 'admin':
        flash('Bạn không có quyền truy cập vào kho hàng!', 'danger')
        return redirect(url_for('dashboard.index'))
    products = Product.query.all()
    return render_template('inventory/products.html', products=products)

@inventory_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        flash('Bạn không có quyền thực hiện hành động này!', 'danger')
        return redirect(url_for('dashboard.index'))
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        sku = request.form.get('sku')
        category_id = request.form.get('category_id')
        price = request.form.get('price')
        cost = request.form.get('cost')
        stock_quantity = request.form.get('stock_quantity')
        
        try:
            price = float(price) if price else 0.0
            cost = float(cost) if cost else 0.0
            stock_quantity = int(stock_quantity) if stock_quantity else 0
            
            new_product = Product(
                name=name, sku=sku, category_id=category_id, 
                price=price, cost=cost, stock_quantity=stock_quantity
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Thêm sản phẩm thành công!', 'success')
            return redirect(url_for('inventory.list_products'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra hoặc mã SKU đã tồn tại.', 'danger')
            
    return render_template('inventory/product_form.html', product=None, categories=categories)

@inventory_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role != 'admin':
        flash('Bạn không có quyền thực hiện hành động này!', 'danger')
        return redirect(url_for('dashboard.index'))
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.sku = request.form.get('sku')
        product.category_id = request.form.get('category_id')
        price = request.form.get('price')
        cost = request.form.get('cost')
        stock_quantity = request.form.get('stock_quantity')
        
        try:
            product.price = float(price) if price else 0.0
            product.cost = float(cost) if cost else 0.0
            product.stock_quantity = int(stock_quantity) if stock_quantity else 0
            
            db.session.commit()
            flash('Cập nhật sản phẩm thành công!', 'success')
            return redirect(url_for('inventory.list_products'))
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra hoặc mã SKU trùng lặp.', 'danger')
            
    return render_template('inventory/product_form.html', product=product, categories=categories)

@inventory_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if current_user.role != 'admin':
        flash('Bạn không có quyền thực hiện hành động này!', 'danger')
        return redirect(url_for('dashboard.index'))
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Đã xóa sản phẩm!', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Không thể xóa sản phẩm này do ràng buộc dữ liệu.', 'danger')
    return redirect(url_for('inventory.list_products'))
