from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("config.Config")

    db.init_app(app)

    #registrar blueprints
    from app.auth.routes import auth_bp
    
    app.register_blueprint(auth_bp)

    return app
