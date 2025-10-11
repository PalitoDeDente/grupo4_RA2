# /algorithms/fifo.py

import time
# Importando a classe base que você criou e ajustou no passo anterior
from core.cache_base import BaseCache 

def _read_from_slow_disk(text_id: int) -> str:
    """
    Função auxiliar que simula a leitura de um arquivo de texto
    de um disco lento, conforme descrito no trabalho.
    """
    print(f"CACHE MISS! Lendo texto {text_id} do disco lento...")
    # Simula a lentidão do disco. Aumente esse valor para tornar a 
    # diferença entre hit e miss mais perceptível.
    time.sleep(0.1) 
    return f"Este é o conteúdo completo do texto de ID {text_id}."

class FIFOCache(BaseCache):
    """
    Implementação do algoritmo de cache First-In, First-Out (FIFO).
    
    Esta classe herda de BaseCache e implementa a lógica de substituição FIFO,
    além do método 'access' obrigatório pela interface.
    """
    def __init__(self, capacity: int = 10):
        # Inicializa a estrutura de dados da classe pai (BaseCache)
        super().__init__(capacity)

    def put(self, key: int, value: str):
        """
        Adiciona um item ao cache. Se o cache estiver cheio, remove o item
        mais antigo (o primeiro que foi inserido) antes de adicionar o novo.
        """
        if key in self.data:
            # Se o item já existe, o FIFO não atualiza sua posição.
            return

        if self.get_size() >= self.capacity:
            # Cache está cheio. Identifica o item mais antigo.
            # Em nossa lista 'order', o mais antigo é sempre o do índice 0.
            oldest_key = self.order.pop(0)
            
            # Remove o item mais antigo do dicionário de dados.
            del self.data[oldest_key]
            print(f"CACHE CHEIO. Removido (FIFO): Texto {oldest_key}")

        # Adiciona o novo item ao dicionário e ao final da lista de ordem.
        self.data[key] = value
        self.order.append(key)

    def access(self, text_id: int) -> tuple[bool, str, float]:
        """
        Acessa um texto, implementando a lógica de cache hit/miss.
        Este método cumpre o "contrato" definido na interface Cache (do Aluno A).
        """
        start_time = time.time()

        if self.is_in_cache(text_id):
            # --- CACHE HIT ---
            content = self.get(text_id)
            print(f"CACHE HIT! Acessando texto {text_id} da memória.")
            is_hit = True
        else:
            # --- CACHE MISS ---
            content = _read_from_slow_disk(text_id)
            self.put(text_id, content) # Adiciona o novo conteúdo ao cache
            is_hit = False
        
        end_time = time.time()
        access_time = end_time - start_time

        # Retorna a tupla no formato exigido pela interface
        return (is_hit, content, access_time)

# --- Bloco de Teste Simples ---
# Para executar este teste: rode 'python algorithms/fifo.py' no terminal
if __name__ == '__main__':
    print("--- Testando o Algoritmo FIFOCache ---")
    # Usando uma capacidade pequena para testar a remoção facilmente
    cache = FIFOCache(capacity=3)

    # 1. Acessando 3 itens para encher o cache (serão 3 misses)
    cache.access(10)
    print(cache)
    cache.access(20)
    print(cache)
    cache.access(30)
    print(f"Estado do Cache: {cache}\n")

    # 2. Acessando um item que já está no cache (deve ser um hit)
    print("--- Acessando item 20 (esperado: HIT) ---")
    hit, content, access_time = cache.access(20)
    print(f"Hit: {hit}, Tempo: {access_time:.4f}s")
    print(f"Estado do Cache: {cache}\n")

    # 3. Acessando um novo item (40), que deve causar um miss
    # e remover o item mais antigo (10)
    print("--- Acessando item 40 (esperado: MISS e remoção do 10) ---")
    hit, content, access_time = cache.access(40)
    print(f"Hit: {hit}, Tempo: {access_time:.4f}s")
    print(f"Estado Final do Cache: {cache}\n")