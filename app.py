# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.db import init_db
from models.models import db, Usuario, Cliente, Proveedor, Producto, Venta
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cambia_esto_por_algo_seguro'

# Inicializar la base de datos
init_db(app)

# ========== RUTAS DE AUTENTICACIÓN CON ORM ==========
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        password = request.form['password'].strip()

        if not usuario or not password:
            flash('Completa todos los campos', 'warning')
            return render_template('login.html')

        try:
            # ORM: Buscar usuario por correo
            user = Usuario.query.filter_by(correo=usuario).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_name'] = user.nombre
                return redirect(url_for('sistema', tab='nueva_venta'))
            else:
                flash('Credenciales incorrectas', 'danger')
                
        except Exception as e:
            flash('Error de conexión a la base de datos', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ========== RUTA PRINCIPAL DEL SISTEMA ==========
@app.route('/sistema')
def sistema():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'nueva_venta')
    
    tab_handlers = {
        'proveedores': proveedores,
        'productos': productos,
        'clientes': clientes,
        'ventas': ventas,
        'reportes': reportes
    }
    
    handler = tab_handlers.get(tab)
    if handler:
        return handler()
    
    return render_template('sistema/index.html', tab=tab)

# ========== NUEVA VENTA CON ORM ==========
@app.route('/sistema/nueva_venta')
def nueva_venta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener todos los productos
    productos = Producto.query.all()
    return render_template('sistema/index.html', tab='nueva_venta', productos=productos)

# ========== CLIENTES CON ORM ==========
@app.route('/sistema/clientes')
def clientes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener clientes ordenados por ID descendente
    clientes_data = Cliente.query.order_by(Cliente.id.desc()).all()
    return render_template('sistema/index.html', tab='clientes', clientes=clientes_data)

#@app.route('/sistema/clientes/agregar', methods=['POST'])
#def agregar_cliente():
    # ORM: Crear nuevo cliente
#    nuevo_cliente = Cliente(
#        dni=request.form['dni'],
#        nombre=request.form['nombre'],
#        telefono=request.form['telefono'],
#        direccion=request.form['direccion'],
#        razon=request.form['razon']
#    )
    
#    try:
#        db.session.add(nuevo_cliente)
#        db.session.commit()
#        flash('Cliente agregado', 'success')
#    except Exception as e:
#        db.session.rollback()
#        flash('Error al agregar cliente: ' + str(e), 'danger')
    
#    return redirect(url_for('sistema', tab='clientes'))

#@app.route('/sistema/clientes/eliminar/<int:id>')
#def eliminar_cliente(id):
    # ORM: Eliminar cliente por ID
#    cliente = Cliente.query.get(id)
#    if not cliente:
#        flash('Cliente no encontrado', 'danger')
#        return redirect(url_for('sistema', tab='clientes'))
    
#    try:
#        db.session.delete(cliente)
#        db.session.commit()
#        flash('Cliente eliminado', 'info')
#    except Exception as e:
#        db.session.rollback()
#        flash('Error al eliminar cliente: ' + str(e), 'danger')
    
#    return redirect(url_for('sistema', tab='clientes'))

# En la función agregar_cliente, agrega estas validaciones:

@app.route('/sistema/clientes/agregar', methods=['POST'])
def agregar_cliente():
    # Obtener y limpiar datos del formulario
    dni = request.form['dni'].strip()
    nombre = request.form['nombre'].strip()
    telefono = request.form['telefono'].strip()
    direccion = request.form['direccion'].strip()
    razon = request.form['razon'].strip()
    
    # 🔴 AGREGAR VALIDACIONES (igual que en productos)
    if not dni:
        flash('El DNI del cliente es requerido', 'danger')
        return redirect(url_for('sistema', tab='clientes'))
    
    if not nombre:
        flash('El nombre del cliente es requerido', 'danger')
        return redirect(url_for('sistema', tab='clientes'))
    
    # ORM: Crear nuevo cliente
    nuevo_cliente = Cliente(
        dni=dni,
        nombre=nombre,
        telefono=telefono,
        direccion=direccion,
        razon=razon
    )
    
    try:
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente agregado', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar cliente: ' + str(e), 'danger')
    
    return redirect(url_for('sistema', tab='clientes'))




# ========== PROVEEDORES CON ORM ==========
@app.route('/sistema/proveedores')
def proveedores():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener proveedores ordenados por ID descendente
    proveedores_data = Proveedor.query.order_by(Proveedor.id.desc()).all()
    return render_template('sistema/index.html', tab='proveedores', proveedores=proveedores_data)

@app.route('/sistema/proveedores/agregar', methods=['POST'])
def agregar_proveedor():
    # ORM: Crear nuevo proveedor
    nuevo_proveedor = Proveedor(
        ruc=request.form['ruc'],
        nombre=request.form['nombre'],
        telefono=request.form['telefono'],
        direccion=request.form['direccion'],
        razon=request.form['razon']
    )
    
    try:
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor agregado', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al agregar proveedor: ' + str(e), 'danger')
    
    return redirect(url_for('sistema', tab='proveedores'))

# ========== PRODUCTOS CON ORM ==========
@app.route('/sistema/productos')
def productos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener productos con información del proveedor usando join
    productos_data = db.session.query(
        Producto, Proveedor.nombre
    ).join(
        Proveedor, Producto.id_proveedor == Proveedor.id
    ).order_by(Producto.id.desc()).all()
    
    # Reestructurar datos para compatibilidad con el template
    productos_formateados = []
    for producto, proveedor_nombre in productos_data:
        productos_formateados.append({
            'id': producto.id,
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad': producto.cantidad,
            'precio': producto.precio,
            'id_proveedor': producto.id_proveedor,
            'proveedor': proveedor_nombre
        })
    
    # ORM: Obtener lista de proveedores
    proveedores_lista = Proveedor.query.order_by(Proveedor.nombre).all()
    
    return render_template('sistema/index.html', tab='productos', 
                         productos=productos_formateados, proveedores=proveedores_lista)

@app.route('/sistema/productos/agregar', methods=['POST'])
def agregar_producto():
    # Validaciones
    codigo = request.form['codigo'].strip()
    descripcion = request.form['descripcion'].strip()
    cantidad_str = request.form['cantidad'].strip()
    precio_str = request.form['precio'].strip()
    id_proveedor = request.form['proveedor'].strip()
    
    if not codigo:
        flash('El código del producto es requerido', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    if not descripcion:
        flash('La descripción del producto es requerida', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    try:
        precio = float(precio_str)
        if precio < 0:
            flash('El precio no puede ser negativo', 'danger')
            return redirect(url_for('sistema', tab='productos'))
    except ValueError:
        flash('El precio debe ser un número válido', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    try:
        cantidad = int(cantidad_str)
        if cantidad < 0:
            flash('La cantidad no puede ser negativa', 'danger')
            return redirect(url_for('sistema', tab='productos'))
    except ValueError:
        flash('La cantidad debe ser un número entero válido', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    # ORM: Crear nuevo producto
    nuevo_producto = Producto(
        codigo=codigo,
        descripcion=descripcion,
        cantidad=cantidad,
        precio=precio,
        id_proveedor=id_proveedor
    )
    
    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto agregado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al guardar el producto: ' + str(e), 'danger')
    
    return redirect(url_for('sistema', tab='productos'))

# ========== VENTAS CON ORM ==========
@app.route('/sistema/ventas')
def ventas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener ventas con información del cliente
    ventas_data = db.session.query(
        Venta, Cliente.nombre
    ).join(
        Cliente, Venta.id_cliente == Cliente.id
    ).order_by(Venta.id.desc()).all()
    
    # Reestructurar datos para compatibilidad con el template
    ventas_formateadas = []
    for venta, cliente_nombre in ventas_data:
        ventas_formateadas.append({
            'id': venta.id,
            'cliente': cliente_nombre,
            'total': venta.total,
            'fecha': venta.fecha
        })
    
    return render_template('sistema/index.html', tab='ventas', ventas=ventas_formateadas)

# ========== REPORTES CON ORM ==========
@app.route('/sistema/reportes')
def reportes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ORM: Obtener ventas para reportes
    ventas_data = db.session.query(
        Venta, Cliente.nombre
    ).join(
        Cliente, Venta.id_cliente == Cliente.id
    ).order_by(Venta.id.desc()).all()
    
    # Reestructurar datos para compatibilidad con el template
    ventas_formateadas = []
    for venta, cliente_nombre in ventas_data:
        ventas_formateadas.append({
            'id': venta.id,
            'cliente': cliente_nombre,
            'total': venta.total,
            'fecha': venta.fecha
        })
    
    return render_template('sistema/index.html', tab='reportes', ventas=ventas_formateadas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
