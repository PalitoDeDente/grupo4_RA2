# /core/cache_base.py

# 1. Importe a interface (o "contrato") criada pelo Aluno A.
from core.cache_abc import Cache

# 2. Renomeie SUA classe para "BaseCache" e faça ela herdar da interface "Cache".
class BaseCache(Cache):
    """
    Estrutura de dados principal do cache, desenvolvida pelo Aluno B.
    Esta classe implementa a interface Cache definida pelo Aluno A.
    
    A lógica de substituição e o método 'access' serão implementados
    nas classes de algoritmos específicos (ex: FIFOCache).
    """
    def __init__(self, capacity: int = 10):
        """
        Inicializa o cache.
        
        Args:
            capacity (int): A capacidade máxima de armazenamento do cache, 
                            conforme especificado no requisito[cite: 29].
        """
        self.capacity = capacity
        # Dicionário para armazenar os dados do cache (id_texto -> conteudo_texto)
        self.data = {}
        # Lista para ajudar a rastrear a ordem de inserção ou uso
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
    
    # IMPORTANTE: Note que o método abstrato 'access' da interface
    # ainda não foi implementado aqui. Isso é correto. A sua próxima
    # classe, FIFOCache, vai herdar de BaseCache e terá a obrigação
    # de implementar o método 'access' para finalmente cumprir o contrato.