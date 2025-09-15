import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask

# --- Funciones Compartidas ---
# Definimos estas funciones aquí para que puedan ser importadas por los blueprints.

def get_conn():
    """Carga las credenciales de la BD desde el entorno y devuelve una conexión."""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def validar_credenciales(usuario, password):
    """Valida las credenciales del usuario según las reglas definidas."""
    if not usuario or not password:
        return False, "Campos vacíos"
    if usuario.lower() in password.lower():
        return False, "La contraseña no debe contener el usuario"
    if len(password) < 8:
        return False, "Mínimo 8 caracteres"
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, "Debe ser alfanumérica"
    return True, ""


# --- Fábrica de la Aplicación ---

def create_app():
    """Crea y configura una instancia de la aplicación Flask."""
    
    # Creamos la app, especificando que las carpetas de plantillas y archivos estáticos
    # están en el directorio padre (fuera de 'src').
    app = Flask(__name__, instance_relative_config=True,
                template_folder='../templates',
                static_folder='../static')

    # Cargamos las variables de entorno desde el archivo .env
    load_dotenv()

    # Configuramos la clave secreta
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # Importamos y registramos los Blueprints
    from . import auth
    from . import main
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)

    return app
