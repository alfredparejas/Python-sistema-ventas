# init_db.py
print("🔧 Inicializando verificación de base de datos...")

# Primero configuramos Flask sin las dependencias circulares
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:App1234!@172.31.176.1:3306/sistemaventas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy directamente
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo Usuario aquí para evitar importaciones circulares
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column('pass', db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

def mysql_password(raw: str) -> str:
    """Devuelve el mismo hash que MySQL PASSWORD('texto')"""
    import hashlib
    if not raw:
        return "*DA39A3EE5E6B0D3255BFEF95601890AFD80709"
    hash1 = hashlib.sha1(raw.encode('utf-8')).digest()
    hash2 = hashlib.sha1(hash1).hexdigest()
    return "*" + hash2.upper()

def init_database():
    with app.app_context():
        try:
            print("🔍 Verificando conexión a la base de datos...")
            
            # Verificar si la tabla usuarios existe y tiene datos
            usuarios_count = Usuario.query.count()
            print(f"✅ Conexión exitosa. Usuarios en sistema: {usuarios_count}")
            
            # Crear usuario admin si no existe
            if not Usuario.query.filter_by(correo='admin@example.com').first():
                admin_password = mysql_password('admin123')
                # Usar SQL directo para evitar problemas con el ORM
                from sqlalchemy import text
                db.session.execute(text(
                    "INSERT INTO usuarios (correo, pass, nombre) VALUES (:correo, :pass, :nombre)"
                ), {
                    'correo': 'admin@example.com',
                    'pass': admin_password,
                    'nombre': 'Administrador'
                })
                db.session.commit()
                print("✅ Usuario admin creado: admin@example.com / admin123")
            else:
                print("✅ Usuario admin ya existe")
            
            print("🎉 Base de datos verificada correctamente")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    init_database()
