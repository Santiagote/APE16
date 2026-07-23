import spacy
from dominio.modelos_oracion import ResultadoAnalisis, Token, Dependencia


class FachadaSpacy:
    def __init__(self):
        self._nlp = spacy.load("es_core_news_sm")

    def analizar(self, oracion: str) -> ResultadoAnalisis:
        doc = self._nlp(oracion)
        resultado = ResultadoAnalisis(oracion=oracion)

        for token in doc:
            resultado.tokens.append(Token(token.text, token.lemma_, token.pos_))
            gobernador = "ROOT" if token.dep_ == "ROOT" else token.head.text
            resultado.dependencias.append(
                Dependencia(gobernador, token.text, token.dep_.lower())
            )

        resultado.arbol_sintactico = self._construir_arbol(doc)
        return resultado

    def _construir_arbol(self, doc) -> str:
        raices = [t for t in doc if t.dep_ == "ROOT"]
        if not raices:
            return ""
        raiz = raices[0]
        return "(ROOT " + self._nodo_arbol(raiz) + ")"

    def _nodo_arbol(self, token) -> str:
        hijos = [h for h in token.children]
        if not hijos:
            return f"({token.pos_} {token.text})"
        partes = [f"({token.pos_} {token.text}"]
        for h in hijos:
            partes.append(self._nodo_arbol(h))
        partes.append(")")
        return " ".join(partes)
