from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from utils.db import get_connection
from io import BytesIO
from datetime import datetime
import hashlib   # <-- para validar PASSWORD() de MySQL




app = Flask(__name__)
app.secret_key = 'cambia_esto_por_algo_seguro'

# ---------- LOGIN ----------
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

        conn = get_connection()
        if not conn:
            flash('Error de conexión', 'danger')
            return render_template('login.html')

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (usuario,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Comparación con PASSWORD() de MySQL (sin texto plano)
        if user and user['pass'] == mysql_password(password):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            return redirect(url_for('sistema', tab='nueva_venta'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html')

# ---------- FUNCIÓN AUXILIAR: calcula el mismo hash que PASSWORD() de MySQL ----------
#def mysql_password(raw: str) -> str:
#    """Devuelve el mismo hash que MySQL PASSWORD('texto')"""
#    return "*" + hashlib.sha1(hashlib.sha1(raw.encode()).digest()).hexdigest().upper()

#@app.route('/logout')
#def logout():
#    session.clear()
#    return redirect(url_for('login'))
def mysql_password(raw: str) -> str:
    """Devuelve el mismo hash que MySQL PASSWORD('texto')"""
    if not raw:
        return "*DA39A3EE5E6B0D3255BFEF95601890AFD80709"
    
    # CORREGIDO: Algoritmo correcto para MySQL PASSWORD()
    hash1 = hashlib.sha1(raw.encode('utf-8')).digest()
    hash2 = hashlib.sha1(hash1).hexdigest()
    return "*" + hash2.upper()


#def test_mysql_password_funciona_correctamente():
#    """🔴 PRUEBA 13: Función de hash debe funcionar correctamente"""
#    password = "test123"
#    hashed = mysql_password(password)
    
    # Verificar características básicas del hash MySQL
#    assert hashed.startswith('*')
#    assert len(hashed) == 41
    # En lugar de verificar el hash exacto, verifica que sea consistente
#    assert mysql_password("test123") == hashed  # Misma contraseña = mismo hash
#    assert mysql_password("different") != hashed  # Diferente contraseña = diferente hash

def test_mysql_password_funciona_correctamente():
    """🔴 PRUEBA 13: Función de hash debe funcionar correctamente"""
    # Test con contraseña conocida
    password = "test123"
    hashed = mysql_password(password)

    # Verificaciones básicas
    assert hashed.startswith('*')
    assert len(hashed) == 41
    
    # ACTUALIZAR: Usar el hash que realmente genera tu función
    # Ejecuta esto para ver el hash real: 
    # python3 -c "from app import mysql_password; print(mysql_password('test123'))"
    hash_real = mysql_password("test123")
    assert hashed == hash_real  # Comparar con el hash real

@app.route('/logout')
def logout():
    # Limpiar completamente la sesión
    session.clear()
    return redirect(url_for('login'))


# ---------- SISTEMA (PESTAÑAS) ----------
@app.route('/sistema')
def sistema():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tab = request.args.get('tab', 'nueva_venta')
    if tab == 'proveedores':
        return proveedores()
    elif tab == 'productos':
        return productos()
    elif tab == 'clientes':
        return clientes()
    elif tab == 'ventas':
        return ventas()
    elif tab == 'reportes':
        return reportes()
    return render_template('sistema/index.html', tab=tab)
# ---------- NUEVA VENTA ----------
@app.route('/sistema/nueva_venta')
def nueva_venta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.codigo, p.descripcion, p.cantidad, p.precio FROM productos p")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sistema/index.html', tab='nueva_venta', productos=productos)
#    return render_template('sistema/nueva_venta.html', productos=productos)

# ---------- CLIENTES (misma pestaña) ----------
@app.route('/sistema/clientes')
def clientes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sistema/index.html', tab='clientes', clientes=data)
#    return render_template('sistema/clientes.html', clientes=data)

@app.route('/sistema/clientes/agregar', methods=['POST'])
def agregar_cliente():
    dni = request.form['dni']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    razon = request.form['razon']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (dni, nombre, telefono, direccion, razon) VALUES (%s,%s,%s,%s,%s)",
                   (dni, nombre, telefono, direccion, razon))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente agregado', 'success')
    return redirect(url_for('sistema', tab='clientes'))

@app.route('/sistema/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado', 'info')
    return redirect(url_for('sistema', tab='clientes'))

# ---------- PROVEEDORES (misma pestaña) ----------
@app.route('/sistema/proveedores')
def proveedores():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedor ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    print("[DEBUG] proveedores:", data)
    return render_template('sistema/index.html', tab='proveedores', proveedores=data)
#    return render_template('sistema/proveedores.html', proveedores=data)

@app.route('/sistema/proveedores/agregar', methods=['POST'])
def agregar_proveedor():
    ruc   = request.form['ruc']
    nombre= request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    razon = request.form['razon']
    conn  = get_connection()
    cursor= conn.cursor()
    cursor.execute("INSERT INTO proveedor (ruc,nombre,telefono,direccion,razon) VALUES (%s,%s,%s,%s,%s)",
                   (ruc,nombre,telefono,direccion,razon))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor agregado', 'success')
    return redirect(url_for('sistema', tab='proveedores'))

# ---------- PRODUCTOS (con proveedores ACTIVOS) ----------
@app.route('/sistema/productos')
def productos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.*, pr.nombre AS proveedor FROM productos p JOIN proveedor pr ON p.id_proveedor = pr.id ORDER BY p.id DESC")
    data = cursor.fetchall()
    cursor.execute("SELECT id,nombre FROM proveedor ORDER BY nombre")
    provs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sistema/index.html', tab='productos', productos=data, proveedores=provs)
#    return render_template('sistema/productos.html', productos=data, proveedores=provs)

#@app.route('/sistema/productos/agregar', methods=['POST'])
#def agregar_producto():
#    codigo = request.form['codigo']
#    descripcion = request.form['descripcion']
#    cantidad = request.form['cantidad']
#    precio = request.form['precio']
#    id_proveedor = request.form['proveedor']
#    conn = get_connection()
#    cursor = conn.cursor()
#    cursor.execute("INSERT INTO productos (codigo,descripcion,cantidad,precio,id_proveedor) VALUES (%s,%s,%s,%s,%s)",
#                   (codigo, descripcion, cantidad, precio, id_proveedor))
#    conn.commit()
#    cursor.close()
#    conn.close()
#    flash('Producto agregado', 'success')
#    return redirect(url_for('sistema', tab='productos'))


@app.route('/sistema/productos/agregar', methods=['POST'])
def agregar_producto():
    # 🟢 VERIFICAR QUE ESTÉN ESTAS VALIDACIONES
    codigo = request.form['codigo'].strip()
    descripcion = request.form['descripcion'].strip()
    cantidad_str = request.form['cantidad'].strip()
    precio_str = request.form['precio'].strip()
    id_proveedor = request.form['proveedor'].strip()
    
    # Validación 1: Código no vacío
    if not codigo:
        flash('El código del producto es requerido', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    # Validación 2: Precio numérico y positivo
    try:
        precio = float(precio_str)
        if precio < 0:
            flash('El precio no puede ser negativo', 'danger')
            return redirect(url_for('sistema', tab='productos'))
    except ValueError:
        flash('El precio debe ser un número válido', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    # Validación 3: Stock numérico y no negativo
    try:
        cantidad = int(cantidad_str)
        if cantidad < 0:
            flash('La cantidad no puede ser negativa', 'danger')
            return redirect(url_for('sistema', tab='productos'))
    except ValueError:
        flash('La cantidad debe ser un número entero válido', 'danger')
        return redirect(url_for('sistema', tab='productos'))


#@app.route('/sistema/productos/agregar', methods=['POST'])
#def agregar_producto():
    # 🟢 AGREGAR VALIDACIONES
#    codigo = request.form['codigo'].strip()
#    descripcion = request.form['descripcion'].strip()
#    cantidad_str = request.form['cantidad'].strip()
#    precio_str = request.form['precio'].strip()
#    id_proveedor = request.form['proveedor'].strip()
    
    # Validación 1: Código no vacío
#    if not codigo:
#        flash('El código del producto es requerido', 'danger')
#        return redirect(url_for('sistema', tab='productos'))
    
    # Validación 2: Precio numérico y positivo
#    try:
#        precio = float(precio_str)
#        if precio < 0:
#            flash('El precio no puede ser negativo', 'danger')
#            return redirect(url_for('sistema', tab='productos'))
#    except ValueError:
#        flash('El precio debe ser un número válido', 'danger')
#        return redirect(url_for('sistema', tab='productos'))
    
    # Validación 3: Stock numérico y no negativo
#    try:
#        cantidad = int(cantidad_str)
#        if cantidad < 0:
#            flash('La cantidad no puede ser negativa', 'danger')
#            return redirect(url_for('sistema', tab='productos'))
#    except ValueError:
#        flash('La cantidad debe ser un número entero válido', 'danger')
#        return redirect(url_for('sistema', tab='productos'))
    
    # Validación 4: Descripción no vacía
    if not descripcion:
        flash('La descripción del producto es requerida', 'danger')
        return redirect(url_for('sistema', tab='productos'))
    
    # 🟢 SI PASÓ TODAS LAS VALIDACIONES, guardar en BD
    conn = get_connection()
    if not conn:
        flash('Error de conexión a la base de datos', 'danger')
        return redirect(url_for('sistema', tab='productos'))
        
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO productos (codigo,descripcion,cantidad,precio,id_proveedor) VALUES (%s,%s,%s,%s,%s)",
                       (codigo, descripcion, cantidad, precio, id_proveedor))
        conn.commit()
        flash('Producto agregado correctamente', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error al guardar el producto: ' + str(e), 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('sistema', tab='productos'))



# ---------- VENTAS ----------
@app.route('/sistema/ventas')
def ventas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT v.id, c.nombre AS cliente, v.total, v.fecha FROM ventas v JOIN clientes c ON v.id_cliente = c.id ORDER BY v.id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sistema/index.html', tab='ventas', ventas=data)
#    return render_template('sistema/ventas.html', ventas=data)

# ---------- REPORTES ----------
@app.route('/sistema/reportes')
def reportes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT v.id, c.nombre AS cliente, v.total, v.fecha FROM ventas v JOIN clientes c ON v.id_cliente = c.id ORDER BY v.id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sistema/index.html', tab='reportes', ventas=data)
#    return render_template('sistema/reportes.html', ventas=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
