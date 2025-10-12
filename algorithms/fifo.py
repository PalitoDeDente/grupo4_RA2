import time
from core.cache_base import BaseCache 

class FIFOCache(BaseCache):
    """
    Implementação do algoritmo de cache First-In, First-Out (FIFO).
    """
    def __init__(self, capacity: int = 10, reader_func=None):
        super().__init__(capacity)
        if reader_func is None:
            raise ValueError("Uma função de leitura (reader_func) deve ser fornecida.")
        self.read_from_slow_disk = reader_func

    def put(self, key: int, value: str):
        """
        Adiciona um item ao cache. Se o cache estiver cheio, remove o item
        mais antigo (o primeiro que foi inserido) antes de adicionar o novo.
        """
        if key in self.data:
            return

        if self.get_size() >= self.capacity:
            oldest_key = self.order.pop(0)
            del self.data[oldest_key]
            print(f"CACHE CHEIO. Removido (FIFO): Texto {oldest_key}")

        self.data[key] = value
        self.order.append(key)

    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa um texto, implementando a lógica de cache hit/miss.
        """
        start_time = time.perf_counter()

        if self.is_in_cache(text_id):
            content = self.get(text_id)
            print(f"CACHE HIT! Acessando texto {text_id} da memória.")
            is_hit = True
        else:
            print(f"CACHE MISS! Lendo texto {text_id} do disco lento...")
            content = self.read_from_slow_disk(text_id)
            self.put(text_id, content)
            is_hit = False
        
        end_time = time.perf_counter()
        access_time = end_time - start_time

        return (is_hit, content, access_time)