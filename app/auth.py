from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/')

# Página principal: Login
@auth_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Aquí puedes implementar la lógica para redirigir al usuario
            return "Bienvenido al sistema, {}.".format(user.username)
        else:
            flash('Credenciales inválidas. Por favor, inténtelo de nuevo.')

    return render_template('login.html')

# Página de registro
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validación de contraseñas
        if password != confirm_password:
            flash('Las contraseñas no coinciden.')
            return redirect(url_for('auth.register'))

        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Por favor, inicie sesión.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
