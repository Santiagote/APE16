from flask import Blueprint, request, jsonify
from dataclasses import asdict
from servicios.clasificador_oraciones import ClasificadorOraciones

controlador_analisis = Blueprint("controlador_analisis", __name__)
servicio = ClasificadorOraciones()

@controlador_analisis.route("/api/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    resultado = servicio.analizar_y_clasificar(data["oracion"])
    payload = asdict(resultado)
    payload["tipo"] = resultado.tipo.value if resultado.tipo else None
    return jsonify(payload)