from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app.models import User  # Import models here to avoid circular import

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from app.routes.general_routes import general_routes
        from app.routes.admin_routes import admin_routes
        from app.routes.employee_routes import employee_routes
        from app.routes.customer_routes import customer_routes
        from app.routes.auth_routes import auth_routes

        app.register_blueprint(general_routes)
        app.register_blueprint(auth_routes, url_prefix='/authentication')
        app.register_blueprint(admin_routes, url_prefix='/admin')
        app.register_blueprint(employee_routes, url_prefix='/employee')
        app.register_blueprint(customer_routes, url_prefix='/customer')

    return app
