from flask import render_template
from flask_login import login_required
from . import pets_bp
from app.models import Customer, Pet

@pets_bp.route('/customers')
@login_required
def list_customers():
    customers = Customer.query.all()
    return render_template('pets/customers.html', customers=customers)

@pets_bp.route('/pets')
@login_required
def list_pets():
    pets = Pet.query.all()
    return render_template('pets/pets.html', pets=pets)
