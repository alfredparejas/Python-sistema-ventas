# models/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column('pass', db.String(100), nullable=False)  # 'pass' es el nombre real en la BD
    nombre = db.Column(db.String(100), nullable=False)
    
    def set_password(self, password_text):
        """Establece la contraseña usando el mismo hash que MySQL PASSWORD()"""
        self.password = self.mysql_password(password_text)
    
    def check_password(self, password_text):
        """Verifica la contraseña"""
        return self.password == self.mysql_password(password_text)
    
    @staticmethod
    def mysql_password(raw: str) -> str:
        """Devuelve el mismo hash que MySQL PASSWORD('texto')"""
        if not raw:
            return "*DA39A3EE5E6B0D3255BFEF95601890AFD80709"
        hash1 = hashlib.sha1(raw.encode('utf-8')).digest()
        hash2 = hashlib.sha1(hash1).hexdigest()
        return "*" + hash2.upper()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    razon = db.Column(db.String(100))
    
    # Relaciones
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id = db.Column(db.Integer, primary_key=True)
    ruc = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    razon = db.Column(db.String(100))
    
    # Relaciones
    productos = db.relationship('Producto', backref='proveedor_rel', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
