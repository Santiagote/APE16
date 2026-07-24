"""
Punto de entrada principal para el servidor Backend en Flask.

Este archivo inicializa la aplicación Flask, habilita el soporte para CORS
(Cross-Origin Resource Sharing) y registra las rutas del controlador de análisis sintáctico.
"""

from flask import Flask
from flask_cors import CORS
from api.controlador_analisis import controlador_analisis

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir peticiones HTTP desde el frontend (Angular u otros clientes)
CORS(app)

# Registro del blueprint que contiene los endpoints de la API REST
app.register_blueprint(controlador_analisis)

if __name__ == "__main__":
    # Ejecuta el servidor de desarrollo en el puerto 5000 con modo depuración activo
    app.run(debug=True, port=5000)