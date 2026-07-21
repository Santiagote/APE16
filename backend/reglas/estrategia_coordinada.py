from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from reglas.estrategia_clasificacion import EstrategiaClasificacion
from reglas import tabla_conectores

class EstrategiaCoordinada(EstrategiaClasificacion):
    def clasificar(self, resultado: ResultadoAnalisis):
        for d in resultado.dependencias:
            if d.relacion == "cc":
                tipo = tabla_conectores.COORDINADAS.get(d.dependiente.lower())
                if tipo:
                    return TipoOracion.COMPUESTA_COORDINADA, tipo
        return None