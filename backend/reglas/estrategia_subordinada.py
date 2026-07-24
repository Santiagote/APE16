"""
Estrategia de clasificación para Oraciones Compuestas Subordinadas.

Busca dependencias de subordinación (`mark` - marker, `advcl` - adverbial clause modifier)
en el grafo Universal Dependencies y las evalúa contra la tabla de conectores subordinados.
"""

from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from reglas.estrategia_clasificacion import EstrategiaClasificacion
from reglas import tabla_conectores


class EstrategiaSubordinada(EstrategiaClasificacion):
    """Estrategia concreta que identifica si una oración es Compuesta Subordinada."""

    def clasificar(self, resultado: ResultadoAnalisis):
        """
        Inspecciona las dependencias sintácticas en busca de marcadores de subordinación (`mark` o `advcl`).

        :param resultado: Objeto con los datos analizados de la oración.
        :return: Tupla (TipoOracion.COMPUESTA_SUBORDINADA, nexo) o None si no aplica.
        """
        for d in resultado.dependencias:
            # 'mark' representa un marcador o conjunción subordinante (ej. 'que', 'porque', 'si')
            # 'advcl' representa una cláusula subordinada adverbial (ej. 'aunque llueva')
            if d.relacion in ("mark", "advcl"):
                tipo = tabla_conectores.SUBORDINADAS.get(d.dependiente.lower())
                if tipo:
                    return TipoOracion.COMPUESTA_SUBORDINADA, tipo
        return None