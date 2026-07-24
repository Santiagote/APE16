"""
Interfaz base para el patrón de diseño Estrategia (Strategy Pattern).

Define la interfaz común que deben implementar todas las estrategias de clasificación
de oraciones basadas en reglas sintácticas y semánticas.
"""

from abc import ABC, abstractmethod
from dominio.modelos_oracion import ResultadoAnalisis


class EstrategiaClasificacion(ABC):
    """Clase abstracta base para las estrategias de clasificación de oraciones."""

    @abstractmethod
    def clasificar(self, resultado: ResultadoAnalisis):
        """
        Evalúa el análisis sintáctico y determina si la oración coincide con esta regla.

        :param resultado: Instancia de ResultadoAnalisis con dependencias y tokens.
        :return: Tupla (TipoOracion, relacion_semantica) si aplica la regla, o None en caso contrario.
        """
        pass