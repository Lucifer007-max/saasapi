from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'saasproject'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u424530452_saas:7|v^LLC34P3Z@srv975.hstgr.io:3306/u424530452_saas_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .start import start
    from .service import service

    app.register_blueprint(start, url_prefix='/')
    app.register_blueprint(service, url_prefix='/api/v1')

    with app.app_context():
        create_database()  # Check and create database tables

    return app

def create_database():
    # Check if tables already exist, then create if they don't
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()

    # db.create_all()
    # print('Database Created Successfully!')

