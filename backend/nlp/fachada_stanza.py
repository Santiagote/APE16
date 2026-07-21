import stanza
from dominio.modelos_oracion import ResultadoAnalisis, Token, Dependencia

class FachadaStanza:
    def __init__(self):
        self._pipeline = stanza.Pipeline(
            lang="es",
            processors="tokenize,pos,lemma,depparse,constituency",
            verbose=False,
        )

    def analizar(self, oracion: str) -> ResultadoAnalisis:
        doc = self._pipeline(oracion)
        resultado = ResultadoAnalisis(oracion=oracion)

        for frase in doc.sentences:
            for w in frase.words:
                resultado.tokens.append(Token(w.text, w.lemma, w.upos))
                gobernador = "ROOT" if w.head == 0 else frase.words[w.head - 1].text
                resultado.dependencias.append(
                    Dependencia(gobernador, w.text, w.deprel)
                )
            if frase.constituency:
                resultado.arbol_sintactico = str(frase.constituency)

        return resultado