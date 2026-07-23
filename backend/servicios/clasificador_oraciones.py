from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from nlp.fachada_stanza import FachadaStanza
from nlp.fachada_spacy import FachadaSpacy
from reglas.estrategia_coordinada import EstrategiaCoordinada
from reglas.estrategia_subordinada import EstrategiaSubordinada


class ClasificadorOraciones:
    def __init__(self):
        self._fachadas = {
            "stanza": FachadaStanza(),
            "spacy": FachadaSpacy(),
        }
        self._estrategias = [EstrategiaCoordinada(), EstrategiaSubordinada()]

    def analizar_y_clasificar(self, oracion: str, motor: str = "stanza") -> ResultadoAnalisis:
        fachada = self._fachadas.get(motor, self._fachadas["stanza"])
        resultado = fachada.analizar(oracion)

        for d in resultado.dependencias:
            rel = d.relacion.lower()
            if rel == "root":
                resultado.verbo_principal = d.dependiente
            elif rel in ("nsubj", "nsubj:pass"):
                resultado.sujeto = d.dependiente
            elif rel in ("obj", "dobj"):
                resultado.objeto_directo = d.dependiente

        for estrategia in self._estrategias:
            clasificacion = estrategia.clasificar(resultado)
            if clasificacion:
                resultado.tipo, resultado.relacion_semantica = clasificacion
                return resultado

        resultado.tipo = TipoOracion.SIMPLE
        return resultado