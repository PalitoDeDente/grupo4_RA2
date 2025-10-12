from core.cache_abc import Cache

class BaseCache(Cache):
    """
    Estrutura de dados principal do cache.
    Esta classe implementa a interface Cache.
    A lógica de substituição e o método 'access' serão implementados
    nas classes de algoritmos específicos.
    """
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache.
        
        Args:
            capacity (int): A capacidade máxima de armazenamento do cache.
        """
        self.capacity = capacity
        self.data = {}
        self.order = []

    def get(self, key: int) -> str | None:
        """
        Recupera um item do cache.
        """
        return self.data.get(key)

    def is_in_cache(self, key: int) -> bool:
        """
        Verifica se um item (texto) já está no cache.
        """
        return key in self.data

    def get_size(self) -> int:
        """
        Retorna o número atual de itens no cache.
        """
        return len(self.data)

    def __str__(self) -> str:
        """
        Representação em string do estado atual do cache.
        """
        items = ', '.join(map(str, self.order))
        return f"Cache (Size: {self.get_size()}/{self.capacity}) -> [{items}]"