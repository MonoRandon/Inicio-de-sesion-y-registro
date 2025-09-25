
from Compañero_de_Viaje.app.config.mysqlconnection import MySQLConnection
from flask import flash

class Viaje:
    def __init__(self, data):
        self.id = data.get('id')
        self.destino = data.get('destino')
        self.descripcion = data.get('descripcion')
        self.fecha_de_viaje_desde = data.get('fecha_de_viaje_desde')
        self.fecha_de_viaje_a = data.get('fecha_de_viaje_a')
        self.usuario_id = data.get('usuario_id')

    # Crear viaje
    @classmethod
    def guardar(cls, data):
        query = """
        INSERT INTO viajes (destino, descripcion, fecha_de_viaje_desde, fecha_de_viaje_a, usuario_id)
        VALUES (%(destino)s, %(descripcion)s, %(fecha_de_viaje_desde)s, %(fecha_de_viaje_a)s, %(usuario_id)s);
        """
        return MySQLConnection('compañero_de_viaje_db').query_db(query, data)

    # Leer viaje por id
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM viajes WHERE id = %(id)s;"
        resultado = MySQLConnection('compañero_de_viaje_db').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    # Leer todos los viajes
    @classmethod
    def obtener_todo(cls):
        query = "SELECT * FROM viajes;"
        resultados = MySQLConnection('compañero_de_viaje_db').query_db(query)
        return [cls(row) for row in resultados] if resultados else []

    # Actualizar viaje
    @classmethod
    def actualizar(cls, data):
        query = """
        UPDATE viajes SET destino=%(destino)s, descripcion=%(descripcion)s, fecha_de_viaje_desde=%(fecha_de_viaje_desde)s, fecha_de_viaje_a=%(fecha_de_viaje_a)s 
        WHERE id=%(id)s;
        """
        return MySQLConnection('compañero_de_viaje_db').query_db(query, data)

    # Eliminar viaje
    @classmethod
    def borrar(cls, datos):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        return MySQLConnection('compañero_de_viaje_db').query_db(query, datos)

    # Validar viaje
    @staticmethod
    def validar_viaje(form):
        is_valid = True
        if not form['destino']:
            flash('El destino es obligatorio.')
            is_valid = False
        if not form['descripcion']:
            flash('La descripción es obligatoria.')
            is_valid = False
        if not form['fecha_de_viaje_desde'] or not form['fecha_de_viaje_desde']:
            flash('Las fechas de viaje son obligatorias.')
            is_valid = False
        elif form['fecha_de_viaje_a'] < form['fecha_de_viaje_a']:
            flash('La fecha de fin debe ser posterior a la de inicio.')
            is_valid = False
        return is_valid
