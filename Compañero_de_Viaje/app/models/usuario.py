
from Compañero_de_Viaje.app.config.mysqlconnection import MySQLConnection
from flask import flash

class Usuario:
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')

    # Crear usuario
    @classmethod
    def guardar(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return MySQLConnection('compañero_de_viaje_db').query_db(query, data)

    # Leer usuario por email
    @classmethod
    def obtener_por_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = MySQLConnection('compañero_de_viaje_db').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    # Leer usuario por id
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = MySQLConnection('compañero_de_viaje_db').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    # Actualizar usuario
    @classmethod
    def actualizar(cls, data):
        query = """
        UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s WHERE id=%(id)s;
        """
        return MySQLConnection('compañero_de_viaje_db').query_db(query, data)

    # Eliminar usuario
    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return MySQLConnection('compañero_de_viaje_db').query_db(query, data)

    # Validar registro
    @staticmethod
    def validar_registro(form):
        is_valid = True
        if len(form['nombre']) < 3:
            flash('El nombre debe tener al menos 3 caracteres.')
            is_valid = False
        if len(form['apellido']) < 3:
            flash('El apellido debe tener al menos 3 caracteres.')
            is_valid = False
        if not form['email']:
            flash('El email es obligatorio.')
            is_valid = False
        if len(form['password']) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.')
            is_valid = False
        if form['password'] != form.get('confirmar', 'Error'):
            flash('Las contraseñas no coinciden.')
            is_valid = False
        return is_valid
