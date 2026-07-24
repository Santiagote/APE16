"""
Estrategia de clasificación para Oraciones Compuestas Coordinadas.

Busca dependencias sintácticas de coordinantes (`cc` - coordination) en el grafo Universal Dependencies
y las contrasta con la tabla de conectores coordinados (Copulativos, Disyuntivos, Adversativos).
"""

from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from reglas.estrategia_clasificacion import EstrategiaClasificacion
from reglas import tabla_conectores


class EstrategiaCoordinada(EstrategiaClasificacion):
    """Estrategia concreta que identifica si una oración es Compuesta Coordinada."""

    def clasificar(self, resultado: ResultadoAnalisis):
        """
        Inspecciona la lista de dependencias buscando arcos `cc` (coordinating conjunction).

        :param resultado: Objeto con los datos analizados de la oración.
        :return: Tupla (TipoOracion.COMPUESTA_COORDINADA, nexo) o None si no aplica.
        """
        for d in resultado.dependencias:
            # 'cc' es la etiqueta de Universal Dependencies para conjunciones coordinantes
            if d.relacion == "cc":
                tipo = tabla_conectores.COORDINADAS.get(d.dependiente.lower())
                if tipo:
                    return TipoOracion.COMPUESTA_COORDINADA, tipo
        return None