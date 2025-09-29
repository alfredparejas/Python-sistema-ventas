# utils/db.py
from flask_sqlalchemy import SQLAlchemy
from models.models import db

def init_db(app):
    """Inicializa la base de datos con la aplicación Flask"""
    
    # Configuración de la base de datos usando tus parámetros actuales
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:App1234!@172.31.176.1:3306/sistemaventas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }
    
    # Inicializar la base de datos con la app
    db.init_app(app)
    
    return db

def get_db():
    """Obtener instancia de la base de datos para uso en contextos"""
    return db
