from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager
from .models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import auth_bp, dashboard_bp, pets_bp, inventory_bp, services_bp, bookings_bp, pos_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pets_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(pos_bp)
    app.register_blueprint(admin_bp)

    return app
