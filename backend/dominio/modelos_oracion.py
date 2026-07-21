from dataclasses import dataclass, field
from enum import Enum

class TipoOracion(Enum):
    SIMPLE = "Simple"
    COMPUESTA_COORDINADA = "Compuesta Coordinada"
    COMPUESTA_SUBORDINADA = "Compuesta Subordinada"

@dataclass
class Token:
    palabra: str
    lema: str
    pos: str

@dataclass
class Dependencia:
    gobernador: str
    dependiente: str
    relacion: str  

@dataclass
class ResultadoAnalisis:
    oracion: str
    tokens: list[Token] = field(default_factory=list)
    dependencias: list[Dependencia] = field(default_factory=list)
    arbol_sintactico: str = ""
    tipo: TipoOracion = None
    relacion_semantica: str = None
    sujeto: str = None
    verbo_principal: str = None
    objeto_directo: str = None