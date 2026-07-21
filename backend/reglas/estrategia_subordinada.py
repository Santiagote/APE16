from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from reglas.estrategia_clasificacion import EstrategiaClasificacion
from reglas import tabla_conectores

class EstrategiaSubordinada(EstrategiaClasificacion):
    def clasificar(self, resultado: ResultadoAnalisis):
        for d in resultado.dependencias:
            if d.relacion in ("mark", "advcl"):
                tipo = tabla_conectores.SUBORDINADAS.get(d.dependiente.lower())
                if tipo:
                    return TipoOracion.COMPUESTA_SUBORDINADA, tipo
        return None