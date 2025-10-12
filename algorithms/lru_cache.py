import time
from collections import OrderedDict
from core.cache_abc import Cache, CacheStats

class LRUCache(Cache):
    """
    Implementação de um cache usando a estratégia Least Recently Used (LRU).
    Utiliza um OrderedDict para manter a ordem de acesso eficientemente.
    """
    def __init__(self, capacity: int = 10, reader_func=None):
        if capacity <= 0:
            raise ValueError("Capacidade do cache deve ser maior que zero.")
        if reader_func is None:
            raise ValueError("Uma função de leitura (reader_func) deve ser fornecida.")
        
        self.capacity = capacity
        self.cache = OrderedDict()
        self.read_from_slow_disk = reader_func
        self._hits = 0
        self._misses = 0
        self._total_access_time = 0.0

    def access(self, text_id: int) -> tuple[bool, str, float]:
        start_time = time.perf_counter()

        if text_id in self.cache:
            self._hits += 1
            self.cache.move_to_end(text_id)
            content = self.cache[text_id]
            is_hit = True
        else:
            self._misses += 1
            content = self.read_from_slow_disk(text_id)

            if len(self.cache) >= self.capacity:
                lru_item = self.cache.popitem(last=False)
                print(f"Cache cheio. Removido (LRU): Texto {lru_item[0]}.")

            self.cache[text_id] = content
            is_hit = False

        end_time = time.perf_counter()
        access_time = end_time - start_time
        self._total_access_time += access_time
        return is_hit, content, access_time

    def get_stats(self) -> CacheStats:
        return CacheStats(
            hits=self._hits,
            misses=self._misses,
            total_access_time=self._total_access_time
        )