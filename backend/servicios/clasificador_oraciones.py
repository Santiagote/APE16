"""
Servicio principal de procesamiento y clasificación sintáctico-semántica de oraciones.

Orquesta la ejecución entre los diferentes motores de NLP (Stanza / spaCy),
identifica los elementos gramaticales principales (sujeto, verbo principal, objeto directo)
y aplica la cadena de estrategias de clasificación (Coordinadas, Subordinadas, Simples).
"""

from dominio.modelos_oracion import ResultadoAnalisis, TipoOracion
from nlp.fachada_stanza import FachadaStanza
from nlp.fachada_spacy import FachadaSpacy
from reglas.estrategia_coordinada import EstrategiaCoordinada
from reglas.estrategia_subordinada import EstrategiaSubordinada


class ClasificadorOraciones:
    """Servicio coordinador que utiliza fachadas NLP y patrones de estrategia."""

    def __init__(self):
        """Inicializa las fachadas de NLP disponibles y la lista ordenada de estrategias."""
        self._fachadas = {
            "stanza": FachadaStanza(),
            "spacy": FachadaSpacy(),
        }
        # Lista priorizada de estrategias de clasificación sintáctica
        self._estrategias = [EstrategiaCoordinada(), EstrategiaSubordinada()]

    def analizar_y_clasificar(self, oracion: str, motor: str = "stanza") -> ResultadoAnalisis:
        """
        Analiza sintácticamente la oración con el motor especificado y aplica las reglas de clasificación.

        :param oracion: Cadena de texto de la oración a analizar.
        :param motor: Nombre del motor NLP a utilizar ("stanza" o "spacy").
        :return: Objeto ResultadoAnalisis completo con la clasificación y roles sintácticos.
        """
        # Seleccionar la fachada correspondiente al motor solicitado (por defecto Stanza)
        fachada = self._fachadas.get(motor, self._fachadas["stanza"])
        resultado = fachada.analizar(oracion)

        # 1. Extraer componentes principales de la oración según etiquetas Universal Dependencies
        for d in resultado.dependencias:
            rel = d.relacion.lower()
            if rel == "root":
                resultado.verbo_principal = d.dependiente
            elif rel in ("nsubj", "nsubj:pass"):
                resultado.sujeto = d.dependiente
            elif rel in ("obj", "dobj"):
                resultado.objeto_directo = d.dependiente

        # 2. Evaluar reglas de clasificación según las estrategias registradas
        for estrategia in self._estrategias:
            clasificacion = estrategia.clasificar(resultado)
            if clasificacion:
                resultado.tipo, resultado.relacion_semantica = clasificacion
                return resultado

        # 3. Si no cumple ninguna regla de coordinación o subordinación, se clasifica como Oración Simple
        resultado.tipo = TipoOracion.SIMPLE
        return resultado