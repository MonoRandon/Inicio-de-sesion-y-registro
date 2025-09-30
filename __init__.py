
from flask import Flask
import os

def create_app():
    ruta_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
    app = Flask(__name__, template_folder=ruta_templates)
    app.secret_key = 'SuperLlaveSecreta >:)'  # Cambia esto en producción

    # Rutas principales para registro, login, logout y éxito
    from flask import render_template, request, redirect, session, flash, url_for
    from app.config.mysqlconnection import MySQLConnection
    import re
    from datetime import datetime, date
    import bcrypt

    DB = 'companero_de_viaje_db'

    def validar_registro(form):
        errores = []
        # Nombre y apellido
        if not form.get('nombre') or len(form['nombre']) < 2 or not form['nombre'].isalpha():
            errores.append('El nombre debe tener al menos 2 letras y solo letras.')
        if not form.get('apellido') or len(form['apellido']) < 2 or not form['apellido'].isalpha():
            errores.append('El apellido debe tener al menos 2 letras y solo letras.')
        # Email
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not form.get('email') or not re.match(email_regex, form['email']):
            errores.append('El email no es válido.')
        else:
            mysql = MySQLConnection(DB)
            existe = mysql.query_db('SELECT id FROM usuarios WHERE email=%s', (form['email'],))
            if existe:
                errores.append('El email ya está registrado.')
        # Password
        password = form.get('password', '')
        if not password or len(password) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            errores.append('La contraseña debe tener al menos una mayúscula.')
        if not re.search(r'\d', password):
            errores.append('La contraseña debe tener al menos un número.')
        if password != form.get('confirmar_password', ''):
            errores.append('Las contraseñas no coinciden.')
        # Fecha de nacimiento (mayor de edad)
        try:
            fecha_nac = datetime.strptime(form.get('fecha_nacimiento',''), '%Y-%m-%d').date()
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            if edad < 18:
                errores.append('Debes ser mayor de edad para registrarte.')
        except:
            errores.append('Fecha de nacimiento inválida.')
        # Género (opcional, pero debe estar en el select)
        if form.get('genero') not in ['Masculino','Femenino','Otro']:
            errores.append('Selecciona un género válido.')
        # Términos
        if not form.get('terminos'):
            errores.append('Debes aceptar los términos y condiciones.')
        return errores

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        errores = validar_registro(request.form)
        if errores:
            for e in errores:
                flash(e, 'error')
            return redirect(url_for('index'))
        pw_hash = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())
        datos = (
            request.form['nombre'],
            request.form['apellido'],
            request.form['email'],
            pw_hash,
            request.form['fecha_nacimiento'],
            request.form['genero'],
            1
        )
        mysql = MySQLConnection(DB)
        user_id = mysql.query_db('INSERT INTO usuarios (nombre, apellido, email, password, fecha_nacimiento, genero, terminos) VALUES (%s,%s,%s,%s,%s,%s,%s)', datos)
        session['user_id'] = user_id
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('exito'))

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form.get('email_login')
        password = request.form.get('password_login')
        mysql = MySQLConnection(DB)
        user = mysql.query_db('SELECT * FROM usuarios WHERE email=%s', (email,))
        if not user:
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('index'))
        user = user[0]
        if not bcrypt.checkpw(password.encode(), user['password'].encode()):
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('index'))
        session['user_id'] = user['id']
        flash('¡Inicio de sesión exitoso!', 'success')
        return redirect(url_for('exito'))

    @app.route('/exito')
    def exito():
        if 'user_id' not in session:
            return redirect(url_for('index'))
        mysql = MySQLConnection(DB)
        usuario = mysql.query_db('SELECT nombre FROM usuarios WHERE id=%s', (session['user_id'],))
        if usuario:
            usuario = usuario[0]
        else:
            usuario = {'nombre': 'Usuario'}
        return render_template('exito.html', usuario=usuario)

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Sesión cerrada correctamente.', 'success')
        return redirect(url_for('index'))

    return app
