from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
dashboard_bp = Blueprint('dashboard', __name__)
pets_bp = Blueprint('pets', __name__)
inventory_bp = Blueprint('inventory', __name__)
services_bp = Blueprint('services', __name__)
bookings_bp = Blueprint('bookings', __name__)
pos_bp = Blueprint('pos', __name__)
admin_bp = Blueprint('admin', __name__)

from . import auth, dashboard, pets, inventory, services, bookings, pos, admin
