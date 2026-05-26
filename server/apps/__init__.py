from flask import Flask
from flask_cors import CORS
from apps.extensions import db, migrate
from apps.config import Config
from apps import models

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from apps.routes import user_bp, category_bp, product_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(product_bp, url_prefix='/api/products')

    return app