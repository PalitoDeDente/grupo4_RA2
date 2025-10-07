from abc import ABC, abstractmethod # Importante a criação de classes abstratas
from typing import NamedTuple # Importando tuplas mais fáceis e claras de acessar para encontrar o valor pelo nome e não índice

# Estrutura de tupla que salva os dados, podendo ser chamados por chaves
class CacheStats(NamedTuple):
    hits: int
    misses: int
    total_access_time: int

class Cache(ABC):
    """
    Essa classe abstrata deverá ser usada como base para implementação do algoritmo de cache
    """

    @abstractmethod
    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa o texto
        Se o texto estiver no cache (hit), retorna o conteúdo
        Se não estiver (miss), deve carregar do disco, armazenar no cache (caso tenha espaço, normal, caso não, de acordo
        com cada tipo de algoritmo de cache) e então retornar o conteúdo.

        Args:
            text_id (int): Identificador numérido do texto (1 a 100)

        Returns:
            Uma tupla contendo:
            - bool: True se for um cache hit e False se foi um cache miss
            - str: Conteúdo do texto solicitado
            - float: O tempo gasto nessa operação de acesso
        """
        pass