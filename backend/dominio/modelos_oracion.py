"""
Modelos de dominio del sistema de análisis gramatical APE16.

Contiene las enumeraciones y estructuras de datos (dataclasses) para representar:
- Tipos de oraciones (Simple, Compuesta Coordinada, Compuesta Subordinada)
- Tokens léxicos y etiquetas morfosintácticas (POS tags)
- Relaciones de dependencia gramatical (Universal Dependencies)
- Resultado consolidado del análisis sintáctico y semántico
"""

from dataclasses import dataclass, field
from enum import Enum


class TipoOracion(Enum):
    """Clasificación sintáctica general de la oración."""
    SIMPLE = "Simple"
    COMPUESTA_COORDINADA = "Compuesta Coordinada"
    COMPUESTA_SUBORDINADA = "Compuesta Subordinada"


@dataclass
class Token:
    """
    Representa una unidad léxica de la oración.
    
    :param palabra: Texto original de la palabra
    :param lema: Forma canónica/base de la palabra
    :param pos: Etiqueta de categoría gramatical (Part-of-Speech Tagging en formato UPOS)
    """
    palabra: str
    lema: str
    pos: str


@dataclass
class Dependencia:
    """
    Representa una relación de dependencia sintáctica dirigida entre dos palabras.
    
    :param gobernador: Palabra origen o núcleo regente (palabra de la que depende)
    :param dependiente: Palabra subordinada o modificadora
    :param relacion: Tipo de relación gramatical (ej. nsubj, obj, cc, mark, root)
    """
    gobernador: str
    dependiente: str
    relacion: str  


@dataclass
class ResultadoAnalisis:
    """
    Objeto contenedor que agrupa toda la información extraída tras el análisis sintáctico.
    
    :param oracion: Texto original analizado
    :param tokens: Lista de tokens con lema y POS tag
    :param dependencias: Arcos de dependencia sintáctica
    :param arbol_sintactico: Representación en notación entre paréntesis (Penn Treebank / LISP)
    :param tipo: Clasificación sintáctica (TipoOracion)
    :param relacion_semantica: Subtipo o nexo de relación (ej. Copulativa, Causal, Condicional)
    :param sujeto: Núcleo del sujeto identificado
    :param verbo_principal: Núcleo verbal principal de la oración (ROOT)
    :param objeto_directo: Objeto o complemento directo identificado
    """
    oracion: str
    tokens: list[Token] = field(default_factory=list)
    dependencias: list[Dependencia] = field(default_factory=list)
    arbol_sintactico: str = ""
    tipo: TipoOracion = None
    relacion_semantica: str = None
    sujeto: str = None
    verbo_principal: str = None
    objeto_directo: str = None