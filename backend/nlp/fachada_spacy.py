"""
Adaptador / Fachada para el motor de procesamiento de lenguaje natural spaCy.

Utiliza el modelo en español `es_core_news_sm` para tokenizar, etiquetar (POS),
extraer árbol de dependencias y construir recursivamente una representación en árbol sintáctico.
"""

import spacy
from dominio.modelos_oracion import ResultadoAnalisis, Token, Dependencia


class FachadaSpacy:
    """Implementa el patrón Fachada (Facade) para encapsular la integración con spaCy."""

    def __init__(self):
        """Inicializa cargando el pipeline en español de spaCy."""
        self._nlp = spacy.load("es_core_news_sm")

    def analizar(self, oracion: str) -> ResultadoAnalisis:
        """
        Procesa una oración en texto plano usando spaCy y transforma los resultados
        al modelo de dominio ResultadoAnalisis.

        :param oracion: Texto a analizar
        :return: Objeto ResultadoAnalisis poblado con tokens, dependencias y árbol sintáctico.
        """
        doc = self._nlp(oracion)
        resultado = ResultadoAnalisis(oracion=oracion)

        # Extraer tokens y construir el grafo de dependencias gramaticales
        for token in doc:
            resultado.tokens.append(Token(token.text, token.lemma_, token.pos_))
            
            # Si el token es la raíz principal (ROOT), su gobernador es marcado como ROOT
            gobernador = "ROOT" if token.dep_ == "ROOT" else token.head.text
            resultado.dependencias.append(
                Dependencia(gobernador, token.text, token.dep_.lower())
            )

        # Generar la representación en árbol entre paréntesis a partir del árbol de dependencias
        resultado.arbol_sintactico = self._construir_arbol(doc)
        return resultado

    def _construir_arbol(self, doc) -> str:
        """
        Construye recursivamente una cadena en formato entre paréntesis (estilo Penn Treebank / LISP)
        a partir del nodo raíz de dependencias en spaCy.
        """
        raices = [t for t in doc if t.dep_ == "ROOT"]
        if not raices:
            return ""
        raiz = raices[0]
        return "(ROOT " + self._nodo_arbol(raiz) + ")"

    def _nodo_arbol(self, token) -> str:
        """Función auxiliar recursiva para dar formato a los nodos y sus hijos sintácticos."""
        hijos = [h for h in token.children]
        if not hijos:
            # Caso base: hoja del árbol (categoría POS + palabra)
            return f"({token.pos_} {token.text})"
        
        # Caso recursivo: nodo intermedio con hijos subordinados
        partes = [f"({token.pos_} {token.text}"]
        for h in hijos:
            partes.append(self._nodo_arbol(h))
        partes.append(")")
        return " ".join(partes)

