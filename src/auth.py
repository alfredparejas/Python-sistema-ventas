from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

# Importaremos las funciones necesarias desde el archivo __init__.py de la app
from . import get_conn, validar_credenciales

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
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

        # La validación segura que implementamos
        if user and check_password_hash(user['pass'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            # Apuntamos a la ruta 'construccion' del blueprint 'main'
            return redirect(url_for('main.construccion'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    # Apuntamos a la ruta 'login' de este mismo blueprint ('auth')
    return redirect(url_for('auth.login'))
