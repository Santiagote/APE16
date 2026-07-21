from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from nlp.fachada_stanza import FachadaStanza
from reglas.estrategia_coordinada import EstrategiaCoordinada
from reglas.estrategia_subordinada import EstrategiaSubordinada

class ClasificadorOraciones:
    def __init__(self):
        self._fachada = FachadaStanza()
        self._estrategias = [EstrategiaCoordinada(), EstrategiaSubordinada()]

    def analizar_y_clasificar(self, oracion: str) -> ResultadoAnalisis:
        resultado = self._fachada.analizar(oracion)

        for estrategia in self._estrategias:
            clasificacion = estrategia.clasificar(resultado)
            if clasificacion:
                resultado.tipo, resultado.relacion_semantica = clasificacion
                return resultado

        resultado.tipo = TipoOracion.SIMPLE
        for d in resultado.dependencias:
            if d.relacion == "root":
                resultado.verbo_principal = d.dependiente
            elif d.relacion == "nsubj":
                resultado.sujeto = d.dependiente
            elif d.relacion == "obj":
                resultado.objeto_directo = d.dependiente
        return resultado