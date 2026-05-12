import logging
from flask import Flask, request
from config import Config
from .extensions import db, migrate, login_manager
from .models import User
from .errors import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info('PetShop Startup')

    # Security Headers Middleware
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Register error handlers
    register_error_handlers(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import auth_bp, dashboard_bp, pets_bp, inventory_bp, services_bp, bookings_bp, pos_bp, admin_bp, reports_bp, pet_sales_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(pos_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(pet_sales_bp)

    return app
