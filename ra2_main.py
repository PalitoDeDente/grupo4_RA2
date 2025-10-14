import time
import os
from algorithms.lru_cache import LRUCache
from algorithms.fifo import FIFOCache
from algorithms.lfu import LFUCache
from algorithms.arc_cache import ARCCache
from simulation.simulator import start_simulation_mode

TEXTS_DIR = "texts"
CONFIG_FILE = "docs/cache_config.txt"

def read_from_slow_disk(text_id: int) -> str:
    """
    Simula a leitura lenta dos arquivos no disco.
    """
    try:
        with open(os.path.join(TEXTS_DIR, f"{text_id}.txt"), 'r', encoding='utf-8-sig') as f:
            content = f.read()
        time.sleep(0.1)
        return content
    except FileNotFoundError:
        return f"Erro: Texto {text_id} não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"

def load_cache_from_config(reader_func):
    """
    Lê o arquivo de configuração e retorna uma instância do cache escolhido.
    Se o arquivo não existir, usa LRUCache como padrão.
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            algorithm_name = f.read().strip()
    except FileNotFoundError:
        print(f"Arquivo de configuração '{CONFIG_FILE}' não encontrado. Usando LRUCache como padrão.")
        algorithm_name = "LRUCache"  # Padrão

    print(f"Carregando algoritmo de cache: {algorithm_name}")

    if algorithm_name == "FIFOCache":
        return FIFOCache(capacity=10, reader_func=reader_func)
    elif algorithm_name == "LFUCache":
        return LFUCache(capacity=10, reader_func=reader_func)
    elif algorithm_name == "ARCCache":
        return ARCCache(capacity=10, reader_func=reader_func)
    elif algorithm_name == "LRUCache":
        return LRUCache(capacity=10, reader_func=reader_func)
    else:
        print(f"Algoritmo '{algorithm_name}' desconhecido. Usando LRUCache como padrão.")
        return LRUCache(capacity=10, reader_func=reader_func)

def main():
    """
    Função principal que executa o laço de interação com o usuário.
    """
    cache_em_uso = load_cache_from_config(read_from_slow_disk)
    print(f"Sistema iniciado com o cache: {type(cache_em_uso).__name__}")
    print("----------------------------------------------------")

    while True:
        try:
            user_input = input("Digite o número do texto (1-100), -1 para simulação ou 0 para sair: ")
            text_id = int(user_input)

            if text_id == 0:
                print("Encerrando...")
                break
            elif text_id == -1:
                # A função de leitura é passada como argumento aqui
                start_simulation_mode(read_from_slow_disk)
                print("\nSimulação concluída. Os gráficos foram salvos na pasta do projeto.")
                print("----------------------------------------------------")
            elif 1 <= text_id <= 100:
                is_hit, content, access_time = cache_em_uso.access(text_id)

                print("\n--- Conteúdo do Texto ---")
                print(content[:500] + "..." if len(content) > 500 else content)
                print("--------------------------------")
                print(f"Status do Cache: {'HIT' if is_hit else 'MISS'}")
                print(f"Tempo de carregamento: {access_time * 1e9:,.0f} nanossegundos.")
                print(f"Estado atual do cache: {cache_em_uso}\n")
            else:
                print("Entrada inválida.\n")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.\n")
def __str__(self) -> str:
        """Retorna uma representação em string do estado atual do cache."""
        items = ', '.join(map(str, self.cache.keys()))
        return f"LRUCache (Size: {len(self.cache)}/{self.capacity}) -> [{items}]"
    
if __name__ == "__main__":
    main()