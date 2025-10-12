import time
from core.cache_base import BaseCache

class LFUCache(BaseCache):
    """
    Implementação do algoritmo de cache Least Frequently Used (LFU).
    """
    def __init__(self, capacity: int = 10, reader_func=None):
        super().__init__(capacity)
        if reader_func is None:
            raise ValueError("Uma função de leitura (reader_func) deve ser fornecida.")
        self.read_from_slow_disk = reader_func
        self.frequency = {}

    def _evict(self):
        """
        Encontra e remove o item menos frequentemente usado.
        """
        min_freq = min(self.frequency.values())
        potential_victims = [key for key, freq in self.frequency.items() if freq == min_freq]
        
        lfu_key = -1
        for key in self.order:
            if key in potential_victims:
                lfu_key = key
                break
        
        print(f"Cache cheio. Removido (LFU): Texto {lfu_key} (frequência: {self.frequency[lfu_key]})")
        
        self.order.remove(lfu_key)
        del self.data[lfu_key]
        del self.frequency[lfu_key]

    def put(self, key: int, value: str):
        """Adiciona um item ao cache, aplicando a política LFU se estiver cheio."""
        if key in self.data:
            return

        if self.get_size() >= self.capacity:
            self._evict()

        self.data[key] = value
        self.order.append(key)
        self.frequency[key] = 1

    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa um texto, atualizando a frequência e aplicando a política LFU.
        """
        start_time = time.perf_counter()

        if self.is_in_cache(text_id):
            print(f"CACHE HIT! Acessando texto {text_id} da memória.")
            content = self.get(text_id)
            self.frequency[text_id] += 1
            is_hit = True
        else:
            print(f"CACHE MISS! Lendo texto {text_id} do disco lento...")
            content = self.read_from_slow_disk(text_id)
            self.put(text_id, content)
            is_hit = False
        
        end_time = time.perf_counter()
        access_time = end_time - start_time

        return (is_hit, content, access_time)