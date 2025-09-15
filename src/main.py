from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirige a la página de login en el blueprint de autenticación
    return redirect(url_for('auth.login'))

@main_bp.route('/construccion')
def construccion():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('construccion.html')
