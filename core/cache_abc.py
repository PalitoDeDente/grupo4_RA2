from abc import ABC, abstractmethod
from typing import NamedTuple

class CacheStats(NamedTuple):
    hits: int
    misses: int
    total_access_time: int

class Cache(ABC):
    """
    Essa classe abstrata deverá ser usada como base para implementação do algoritmo de cache.
    """

    @abstractmethod
    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa o texto.
        Se o texto estiver no cache (hit), retorna o conteúdo.
        Se não estiver (miss), deve carregar do disco, armazenar no cache e retornar o conteúdo.

        Args:
            text_id (int): Identificador numérico do texto (1 a 100).

        Returns:
            Uma tupla contendo:
            - bool: True se for um cache hit e False se foi um cache miss.
            - str: Conteúdo do texto solicitado.
            - float: O tempo gasto nessa operação de acesso.
        """
        pass