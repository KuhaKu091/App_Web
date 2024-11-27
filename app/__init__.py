from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'

    db.init_app(app)

    # Registrar Blueprints
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app
