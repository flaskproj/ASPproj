import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail with your app instance


    # Register blueprints
    from app.routes.general_routes import general_routes
    from app.routes.admin_routes import admin_routes
    from app.routes.employee_routes import employee_routes
    from app.routes import customer_routes

    app.register_blueprint(general_routes)
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(employee_routes, url_prefix='/employee')
    app.register_blueprint(customer_routes, url_prefix='/customer')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
