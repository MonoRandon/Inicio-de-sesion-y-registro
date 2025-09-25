
from flask import Blueprint, render_template, redirect, request, session, flash
from Compañero_de_Viaje.app.models.viajes import Viaje

# Blueprint para viajes
viajes_bp = Blueprint('trips', __name__)

# Leer todos los viajes (Dashboard)
@viajes_bp.route('/dashboard')
def dashboard():
    viajes = Viaje.obtener_todo()
    return render_template('dashboard.html', viajes=viajes)

# Mostrar formulario para crear viaje
@viajes_bp.route('/agregarviaje')
def add_trip():
    return render_template('agregar_viaje.html')

# Crear viaje
@viajes_bp.route('/crearviaje', methods=['POST'])
def crear_viaje():
    if not Viaje.validar_viaje(request.form):
        return redirect('/agregarviaje')
    data = {
        'destino': request.form['destino'],
        'descripcion': request.form['descripcion'],
        'fecha_de_viaje_desde': request.form['fecha_de_viaje_desde'],
        'fecha_de_viaje_a': request.form['fecha_de_viaje_a'],
        'usuario_id': session['user_id']
    }
    Viaje.guardar(data)
    return redirect('/dashboard')

# Leer viaje por id (ver detalles)
@viajes_bp.route('/vista/<int:viaje_id>')
def ver_viaje(viaje_id):
    viaje = Viaje.obtener_por_id({'id': viaje_id})
    return render_template('ver_viaje.html', viaje=viaje)

# Mostrar formulario para editar viaje
@viajes_bp.route('/editarviaje/<int:viaje_id>')
def editar_viaje_form(viaje_id):
    viaje = Viaje.obtener_por_id({'id': viaje_id})
    return render_template('agregar_viaje.html', viaje=viaje)

# Actualizar viaje
@viajes_bp.route('/actualizarviaje/<int:viaje_id>', methods=['POST'])
def actualizar_viaje(viaje_id):
    if not Viaje.validar_viaje(request.form):
        return redirect(f'/editarviaje/{viaje_id}')
    data = {
        'id': viaje_id,
        'destino': request.form['destino'],
        'descripcion': request.form['descripcion'],
        'fecha_de_viaje_desde': request.form['fecha_de_viaje_desde'],
        'fecha_de_viaje_a': request.form['fecha_de_viaje_a']
    }

    Viaje.actualizar(data)
    flash('Viaje actualizado correctamente')
    return redirect('/dashboard')

# Eliminar viaje
@viajes_bp.route('/borrarviaje/<int:viaje_id>', methods=['POST'])
def borrar_viaje(viaje_id):
    Viaje.borrar({'id': viaje_id})
    flash('Viaje eliminado')
    return redirect('/dashboard')
