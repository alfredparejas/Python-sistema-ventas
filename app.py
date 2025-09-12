from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'cambia_por_algo_seguro'

# ---------- CONFIG DB ----------
DB = {
    'host': '172.31.176.1',
    'user': 'app_user',
    'password': 'App1234!',
    'database': 'sistemaventa'
}

def get_conn():
    return mysql.connector.connect(**DB)

# ---------- VALIDACIONES ----------
def validar_credenciales(usuario, password):
    if not usuario or not password:
        return False, "Campos vacíos"
    if usuario.lower() in password.lower():
        return False, "La contraseña no debe contener el usuario"
    if len(password) < 8:
        return False, "Mínimo 8 caracteres"
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return False, "Debe ser alfanumérica"
    return True, ""

# ---------- RUTAS ----------
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        ok, msg = validar_credenciales(usuario, password)
        if not ok:
            return render_template('login.html', error=msg)

        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (usuario,))
        user = cur.fetchone()
        cur.close()
        conn.close()

#        if user and check_password_hash(user['pass'], password):
        if user and (user['pass'] == password or check_password_hash(user['pass'], password)):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            return redirect(url_for('construccion'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")

    return render_template('login.html')

@app.route('/construccion')
def construccion():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('construccion.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
