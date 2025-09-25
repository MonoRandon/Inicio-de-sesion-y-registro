
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from Compañero_de_Viaje.app.models.usuario import Usuario

# Blueprint para usuarios
usuario_bp = Blueprint('usuario', __name__)

# Mostrar formulario de registro y login
@usuario_bp.route('/')
def index():
    return render_template('index.html')

# Crear usuario (Registro)
@usuario_bp.route('/register', methods=['POST'])
def crear_usuario():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    usuario_id = Usuario.guardar(data)
    session['user_id'] = usuario_id
    return redirect('/dashboard')

# Leer usuario (Login)
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    usuario = Usuario.obtener_por_email({'email': request.form['email']})
    if not usuario or usuario.password != request.form['password']:
        flash('Credenciales inválidas')
        return redirect('/')
    session['user_id'] = usuario.id
    return redirect('/dashboard')

# Actualizar usuario (Ejemplo: actualizar perfil)
@usuario_bp.route('/actualizar', methods=['POST'])
def actualizar_usuario():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id'],
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email']
    }
    Usuario.actualizar(data)
    flash('Perfil actualizado correctamente')
    return redirect('/dashboard')

# Eliminar usuario 
@usuario_bp.route('/borrar', methods=['POST'])
def eliminar_usuario():
    if 'user_id' not in session:
        return redirect('/')
    Usuario.borrar({'id': session['user_id']})
    session.clear()
    flash('Cuenta eliminada')
    return redirect('/')

# Cerrar sesión
@usuario_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
