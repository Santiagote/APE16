"""
Tabla de clasificación de conectores gramaticales y nexos para idioma español.

Mapea nexos gramaticales a sus respectivas relaciones semánticas para:
- Oraciones compuestas coordinadas (Copulativas, Disyuntivas, Adversativas)
- Oraciones compuestas subordinadas (Causales, Condicionales, Concesivas, Temporales, Finales, Consecutivas)
"""

# Diccionario de conectores para oraciones coordinadas
COORDINADAS = {
    "y": "Copulativa", 
    "e": "Copulativa", 
    "ni": "Copulativa",
    "o": "Disyuntiva", 
    "u": "Disyuntiva",
    "pero": "Adversativa", 
    "sin embargo": "Adversativa",
}

# Diccionario de conectores/conjunciones para oraciones subordinadas
SUBORDINADAS = {
    "porque": "Causal", 
    "ya que": "Causal", 
    "puesto que": "Causal",
    "si": "Condicional", 
    "aunque": "Concesiva",
    "mientras": "Temporal", 
    "cuando": "Temporal",
    "para que": "Final", 
    "por lo tanto": "Consecutiva",
}