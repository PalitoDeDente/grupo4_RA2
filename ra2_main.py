import time
import os

from core.cache_abc import Cache
from algorithms.lru_cache import LRUCache

TEXTS_DIR = "texts" # Diretório onde os 100 textos estão armazenados

def read_from_slow_disk(text_id: int) -> str:
    """
    Simula a leitura lenta dos arquivos no disco
    """
    print(f"Cache Miss! Lendo texto {text_id} do disco lento...")
    try:
        with open(os.path.join(TEXTS_DIR, f"{text_id}.txt"), 'r', encoding='utf-8-sig') as f:
            content = f.read()
        # Simula a lentidão do disco forense [cite: 19, 296]
        time.sleep(0.5) # Atraso artificial de 0.5 segundos
        return content
    except FileNotFoundError:
        return f"Erro: Texto {text_id} não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"

def run_simulation():
    """Placeholder para o modo de simulação a ser implementado pelo aluno D"""
    print("\n--- Modo de simulação ---")
    print("Esta funcionalidade será implementada pelo Aluno D.")
    # O Aluno D irá implementar a lógica de simulação aqui
    print("--------------------------\n")

def main():
    ## TODO: Aqui vamos instanciar o cache escolhido
    ## Por enquanto, vamos simular o comportamente sem um cache real
    cache: Cache = LRUCache(capacity=10)
    print("Usando algoritmo de cache: LRU")

    while True:
        try:
            user_input = input("Digite o número do texto (1-100), -1 para  simulação ou 0 para sair: ")
            text_id = int(user_input)

            if text_id == 0:
                final_stats = cache.get_stats()
                print("\n--- Estatísticas Finais da Sessão ---")
                print(f"Cache Hits: {final_stats.hits}")
                print(f"Cache Misses: {final_stats.misses}")
                print(f"Tempo total de acesso (acumulado): {final_stats.total_access_time:.4f}s")
                print("------------------------------------")
                print("Encerrando o programa.")
                break
            elif text_id == -1:
                run_simulation()
            elif 1 <= text_id <= 100:
                is_hit, content, access_time = cache.access(text_id)

                hit_status = "HIT" if is_hit else "MISS"
                print(f"\n--- Acesso ao Texto {text_id} (Cache {hit_status}) ---")
                print(content[:500] + "..." if len(content) > 500 else content)
                print("---------------------------------------")
                print(f"Tempo de carregamento desta operação: {access_time:.4f} segundos.\n")
            else:
                print("Entrada inválida. Por favor, digite um número entre 1 e 100 para leitura dos textos, -1 para simulação e 0 para encerrar o programa.\n")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número. ")

if __name__ == "__main__":
    main()

