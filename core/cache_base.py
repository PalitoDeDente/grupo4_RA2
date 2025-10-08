# /core/cache_base.py

class Cache:
    """
    Classe base para a estrutura de cache.
    
    Esta classe gerencia o armazenamento dos textos e a capacidade máxima do cache.
    A lógica de substituição (eviction policy) será implementada nas classes filhas.
    """
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache.
        
        Args:
            capacity (int): A capacidade máxima de armazenamento do cache, 
                            conforme especificado no requisito (máximo de dez textos).
        """
        self.capacity = capacity
        # Dicionário para armazenar os dados do cache (id_texto -> conteudo_texto)
        # Oferece acesso rápido O(1) em média.
        self.data = {}
        # Lista para ajudar a rastrear a ordem de inserção ou uso,
        # essencial para algoritmos como FIFO e LRU.
        self.order = []

    def get(self, key: int) -> str | None:
        """
        Recupera um item do cache.
        
        Args:
            key (int): O identificador do texto.
            
        Returns:
            str | None: O conteúdo do texto se encontrado, caso contrário None.
        """
        return self.data.get(key)

    def is_in_cache(self, key: int) -> bool:
        """
        Verifica se um item (texto) já está no cache.
        
        Args:
            key (int): O identificador do texto.
            
        Returns:
            bool: True se o item está no cache, False caso contrário.
        """
        return key in self.data

    def get_size(self) -> int:
        """
        Retorna o número atual de itens no cache.
        
        Returns:
            int: O tamanho atual do cache.
        """
        return len(self.data)

    def __str__(self) -> str:
        """
        Representação em string do estado atual do cache.
        """
        items = ', '.join(map(str, self.order))
        return f"Cache (Size: {self.get_size()}/{self.capacity}) -> [{items}]"