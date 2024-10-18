from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'saasproject'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://u424530452_saas:7|v^LLC34P3Z@srv975.hstgr.io:3306/u424530452_saas_db'



    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://TouchBioDbAdmin:gPiLQFgPHoVpcu5gWQd7@touchbio-db-stage.cxecy80m6y3i.ap-southeast-2.rds.amazonaws.com/touchbio'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .start import start
    from .otpservice import otpservice
    from .authservice import authservice
    app.register_blueprint(start, url_prefix='/')
    app.register_blueprint(otpservice, url_prefix='/api/v1')
    app.register_blueprint(authservice, url_prefix='/api/v1')
    
    
    with app.app_context():
        if not inspect(db.engine).has_table("otp") and inspect(db.engine).has_table("token") :
            create_database()

    return app

def create_database():
    db.drop_all()
    db.create_all()
    print('Database Created Successfully!')
