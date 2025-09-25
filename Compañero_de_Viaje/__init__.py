from flask import Flask
from Compañero_de_Viaje.app.controllers.usuario_controller import usuario_bp
from Compañero_de_Viaje.app.controllers.viajes_controller import viajes_bp

def create_app():
	app = Flask(__name__)
	app.secret_key = 'SuperLlaveSecreta >:)'
	app.register_blueprint(usuario_bp)
	app.register_blueprint(viajes_bp)
	return app
