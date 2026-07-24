"""
Adaptador / Fachada para el motor de procesamiento de lenguaje natural Stanza (Stanford NLP).

Inicializa un pipeline multilenguaje (español) configurado con procesadores de:
- Tokenización (`tokenize`)
- Etiquetado de partes de la oración (`pos`)
- Lematización (`lemma`)
- Análisis de dependencias sintácticas (`depparse`)
- Análisis de constituyentes sintácticos nativo (`constituency`)
"""

import stanza
from dominio.modelos_oracion import ResultadoAnalisis, Token, Dependencia


class FachadaStanza:
    """Implementa el patrón Fachada (Facade) para encapsular la integración con Stanza."""

    def __init__(self):
        """Inicializa y descarga/carga el pipeline de Stanza para idioma español."""
        self._pipeline = stanza.Pipeline(
            lang="es",
            processors="tokenize,pos,lemma,depparse,constituency",
            verbose=False,
        )

    def analizar(self, oracion: str) -> ResultadoAnalisis:
        """
        Procesa una oración utilizando el pipeline de Stanza.

        :param oracion: Texto plano a analizar
        :return: Objeto ResultadoAnalisis con tokens, dependencias y árbol de constituyentes nativo.
        """
        doc = self._pipeline(oracion)
        resultado = ResultadoAnalisis(oracion=oracion)

        # Iterar sobre las oraciones procesadas en el documento
        for frase in doc.sentences:
            for w in frase.words:
                resultado.tokens.append(Token(w.text, w.lemma, w.upos))
                
                # En Stanza, un head == 0 indica la raíz de la oración (ROOT)
                gobernador = "ROOT" if w.head == 0 else frase.words[w.head - 1].text
                resultado.dependencias.append(
                    Dependencia(gobernador, w.text, w.deprel)
                )
            
            # Si Stanza generó un árbol de constituyentes (constituency tree), se convierte a string
            if frase.constituency:
                resultado.arbol_sintactico = str(frase.constituency)

        return resultado