from abc import ABC, abstractmethod
from dominio.modelos_oracion import ResultadoAnalisis

class EstrategiaClasificacion(ABC):
    @abstractmethod
    def clasificar(self, resultado: ResultadoAnalisis):
        """Devuelve (tipo, relacion) si aplica, o None."""