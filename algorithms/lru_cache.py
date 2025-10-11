import time
from collections import OrderedDict

from core.cache_abc import Cache, CacheStats

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ra2_main import read_from_slow_disk


class LRUCache(Cache):
    """
    Implementação de um cache usando a estratégia Least Recently Used (LRU).
    Utiliza um OrderedDict para manter a ordem de acesso eficientemente.
    """

    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("Capacidade do cache deve ser maior que zero.")
        self.capacity = capacity
        self.cache = OrderedDict()
        self._hits = 0
        self._misses = 0
        self._total_access_time = 0.0

    def access(self, text_id: int) -> tuple[bool, str, float]:
        start_time = time.time()

        if text_id in self.cache:
            # --- Cache Hit --- [cite: 333]
            self._hits += 1
            # Move o item acessado para o final para marcá-lo como o mais recentemente usado
            self.cache.move_to_end(text_id)
            content = self.cache[text_id]
            end_time = time.time()
            self._total_access_time += (end_time - start_time)
            return True, content, (end_time - start_time)
        else:
            # --- Cache Miss --- [cite: 338]
            self._misses += 1

            # Carrega o conteúdo do disco lento
            content = read_from_slow_disk(text_id)

            if len(self.cache) >= self.capacity:
                # Evicção: remove o item mais antigo (o primeiro do OrderedDict)
                lru_item = self.cache.popitem(last=False)
                print(f"Cache cheio. Evitando o texto {lru_item[0]} (LRU).")

            # Adiciona o novo item ao cache
            self.cache[text_id] = content

            end_time = time.time()
            self._total_access_time += (end_time - start_time)
            return False, content, (end_time - start_time)

    def get_stats(self) -> CacheStats:
        return CacheStats(
            hits=self._hits,
            misses=self._misses,
            total_access_time=self._total_access_time
        )

# Bloco para testes unitários locais 
if __name__ == '__main__':
    print("--- Executando Testes Unitários Locais para LRUCache ---")

    # Simula a existência dos textos para o teste
    if not os.path.exists('texts'):
        os.makedirs('texts')
    for i in range(1, 15):
        with open(f'texts/{i}.txt', 'w') as f:
            f.write(f"Este é o conteúdo do texto {i}.")

    lru = LRUCache(capacity=3)

    print("\n1. Preenchendo o cache...")
    lru.access(1) # Miss
    lru.access(2) # Miss
    lru.access(3) # Miss
    print(f"Cache state: {list(lru.cache.keys())}") # Esperado: [1, 2, 3]

    print("\n2. Testando Cache Hit e reordenação...")
    lru.access(1) # Hit, 1 deve ir para o final
    print(f"Cache state: {list(lru.cache.keys())}") # Esperado: [2, 3, 1]

    print("\n3. Testando Evicção...")
    lru.access(4) # Miss, deve evitar o 2 (LRU)
    print(f"Cache state: {list(lru.cache.keys())}") # Esperado: [3, 1, 4]

    stats = lru.get_stats()
    print(f"\nEstatísticas Finais: Hits={stats.hits}, Misses={stats.misses}") # Esperado: Hits=1, Misses=4
    print("--- Testes Concluídos ---")