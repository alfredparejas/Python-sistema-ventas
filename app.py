from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import os
from functools import wraps

app = Flask(__name__)

# --- MEJORA 1: Usar variables de entorno para datos sensibles ---
# En tu terminal, antes de correr la app, configura estas variables:
# set SECRET_KEY='tu_clave_super_secreta' (en Windows CMD)
# export SECRET_KEY='tu_clave_super_secreta' (en Linux/macOS/Git Bash)
# Haz lo mismo para DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app.secret_key = os.environ.get('SECRET_KEY', 'valor_por_defecto_solo_para_desarrollo')

# ---------- CONFIG DB MEJORADA ----------
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'app_user'),
    'password': os.environ.get('DB_PASSWORD', 'App1234!'),
    'database': os.environ.get('DB_NAME', 'sistemaventa')
}

def get_conn():
    """Obtiene una conexión a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)

# --- MEJORA 2: Decorador para proteger rutas ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- VALIDACIONES MEJORADAS ----------
def validar_login(usuario, password):
    """Validación simple para el formulario de login."""
    if not usuario or not password:
        return False, "El correo y la contraseña son obligatorios."
    return True, ""

def validar_registro(usuario, password):
    """Validación de complejidad para un futuro formulario de registro."""
    if usuario.lower() in password.lower():
        return False, "La contraseña no debe contener el nombre de usuario."
    if len(password) < 8:
        return False, "La contraseña debe tener mínimo 8 caracteres."
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener letras y números."
    return True, ""

# ---------- RUTAS ----------
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está logueado, redirigir a la página principal
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        # MEJORA 3: Usar la validación correcta para el login
        is_valid, msg = validar_login(usuario, password)
        if not is_valid:
            return render_template('login.html', error=msg)

        conn = None # Inicializar conn a None
        try:
            # MEJORA 4: Manejo seguro de la conexión a la DB
            conn = get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE correo = %s", (usuario,))
            user = cur.fetchone()
            cur.close()
        except mysql.connector.Error as err:
            print(f"Error de base de datos: {err}")
            return render_template('login.html', error="Error en el servidor. Intente más tarde.")
        finally:
            if conn and conn.is_connected():
                conn.close()

        # MEJORA 5: Verificación de contraseña ÚNICAMENTE con hash
        if user and check_password_hash(user['pass'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos.")

    return render_template('login.html')

# Renombramos 'construccion' a 'dashboard' para mayor claridad
@app.route('/dashboard')
@login_required # MEJORA 2: Usando el decorador para proteger la ruta
def dashboard():
    return render_template('construccion.html') # Puedes cambiar esto por dashboard.html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- (Opcional) Ruta para crear un usuario de prueba con contraseña hasheada ---
# Accede a /crear_usuario_test para crear un usuario y poder hacer login
@app.route('/crear_usuario_test')
def crear_usuario_test():
    conn = get_conn()
    cur = conn.cursor()
    
    # Hasheamos la contraseña antes de guardarla
    password_plana = "password123"
    password_hash = generate_password_hash(password_plana)
    
    try:
        # Reemplaza con datos de prueba
        sql = """
            INSERT INTO usuarios (nombre, correo, pass) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE pass=%s;
        """
        valores = ('Usuario de Prueba', 'test@example.com', password_hash, password_hash)
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        return "Usuario de prueba 'test@example.com' con contraseña 'password123' creado/actualizado con éxito."
    except mysql.connector.Error as err:
        return f"Error al crear usuario de prueba: {err}"


if __name__ == '__main__':
    # El modo debug debe estar desactivado en producción
    app.run(host='0.0.0.0', port=5000, debug=True)








