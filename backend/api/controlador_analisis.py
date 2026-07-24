"""
Controlador API REST para la gestión de solicitudes de análisis gramatical y sintáctico.

Define las rutas (endpoints) expuestas por el backend para procesar oraciones
mediante los motores NLP (Stanza / spaCy) y devolver el resultado clasificado.
"""

from flask import Blueprint, request, jsonify
from dataclasses import asdict
from servicios.clasificador_oraciones import ClasificadorOraciones

# Blueprint de Flask para modularizar las rutas de análisis sintáctico
controlador_analisis = Blueprint("controlador_analisis", __name__)

# Instancia del servicio principal de clasificación de oraciones
servicio = ClasificadorOraciones()

@controlador_analisis.route("/api/analizar", methods=["POST"])
def analizar():
    """
    Endpoint HTTP POST /api/analizar

    Recibe un JSON con la estructura:
        {
            "oracion": "Texto a analizar",
            "motor": "stanza" | "spacy"  (opcional, por defecto "stanza")
        }

    Retorna:
        JSON con los tokens, dependencias sintácticas, árbol sintáctico,
        elementos gramaticales (sujeto, verbo, objeto) y tipo de oración.
    """
    data = request.get_json()
    
    # Extraer parámetros de la solicitud con valores por defecto
    oracion = data.get("oracion", "")
    motor = data.get("motor", "stanza")

    # Ejecutar procesamiento NLP y clasificación gramatical
    resultado = servicio.analizar_y_clasificar(oracion, motor=motor)
    
    # Convertir la dataclass ResultadoAnalisis a un diccionario JSON
    payload = asdict(resultado)
    
    # Convertir el valor Enum del tipo de oración a cadena de texto (string)
    payload["tipo"] = resultado.tipo.value if resultado.tipo else None
    
    return jsonify(payload)