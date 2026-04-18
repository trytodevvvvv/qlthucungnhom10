from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
dashboard_bp = Blueprint('dashboard', __name__)
pets_bp = Blueprint('pets', __name__)

from . import auth, dashboard, pets
