import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from core.cache_abc import Cache
from algorithms.fifo import FIFOCache
from algorithms.lru_cache import LRUCache
from algorithms.lfu import LFUCache

def _pattern_pure_random() -> int:
    """Retorna um ID de texto de 1 a 100, com distribuição uniforme."""
    return random.randint(1, 100)

def _pattern_poisson(media=30) -> int:
    """Retorna um ID de texto seguindo uma distribuição de Poisson."""
    num = np.random.poisson(media)
    return max(1, min(100, num))

def _pattern_weighted() -> int:
    """Retorna um ID de texto com 43% de chance para os textos 30-40."""
    if random.random() < 0.43:
        return random.randint(30, 40)
    else:
        outros_textos = list(range(1, 30)) + list(range(41, 101))
        return random.choice(outros_textos)

def run_single_simulation(cache_instance: Cache) -> list:
    """Executa a simulação completa para uma única instância de cache."""
    print(f"\n--- Iniciando simulação para {type(cache_instance).__name__} ---")
    results = []
    patterns = {
        "Aleatório Puro": _pattern_pure_random,
        "Poisson": _pattern_poisson,
        "Ponderado": _pattern_weighted
    }

    for pattern_name, pattern_func in patterns.items():
        print(f"  Testando com o padrão: {pattern_name}...")
        for user in range(1, 4):
            for request_num in range(200):
                text_id = pattern_func()
                is_hit, _, access_time = cache_instance.access(text_id)
                
                results.append({
                    'algorithm': type(cache_instance).__name__,
                    'pattern': pattern_name,
                    'user': user,
                    'text_id': text_id,
                    'is_hit': is_hit,
                    'time': access_time
                })
    
    print(f"--- Simulação para {type(cache_instance).__name__} concluída. ---")
    return results

def analyze_and_plot(all_results: list):
    """Analisa os resultados e gera os gráficos."""
    if not all_results:
        print("Nenhum resultado para analisar.")
        return
    df = pd.DataFrame(all_results)

    plt.figure(figsize=(12, 7))
    sns.barplot(data=df, x='algorithm', y='is_hit', hue='pattern', estimator=sum, errorbar=None)
    plt.title('Total de Cache Hits por Algoritmo e Padrão de Acesso')
    plt.ylabel('Número Total de Hits')
    plt.xlabel('Algoritmo de Cache')
    plt.tight_layout()
    plt.savefig('comparacao_hits.png')
    print("Gráfico 'comparacao_hits.png' gerado.")

    plt.figure(figsize=(12, 7))
    sns.barplot(data=df, x='algorithm', y='time', hue='pattern')
    plt.title('Tempo Médio de Acesso por Algoritmo e Padrão')
    plt.ylabel('Tempo Médio de Acesso (s)')
    plt.xlabel('Algoritmo de Cache')
    plt.tight_layout()
    plt.savefig('comparacao_tempo.png')
    print("Gráfico 'comparacao_tempo.png' gerado.")

    df_misses = df[(df['is_hit'] == False) & (df['pattern'] == 'Ponderado')]
    misses_per_text = df_misses['text_id'].value_counts().nlargest(15)
    
    plt.figure(figsize=(12, 7))
    misses_per_text.plot(kind='bar')
    plt.title('Top 15 Textos com Mais Cache Misses (Padrão Ponderado)')
    plt.ylabel('Número de Misses')
    plt.xlabel('ID do Texto')
    plt.tight_layout()
    plt.savefig('analise_misses_por_texto.png')
    print("Gráfico 'analise_misses_por_texto.png' gerado.")


def analyze_and_save_best_algorithm(all_results: list):
    """
    Analisa os resultados para encontrar o melhor algoritmo e salva a escolha.
    Critério: maior número total de cache hits.
    """
    if not all_results:
        print("Nenhum resultado para analisar e salvar.")
        return

    df = pd.DataFrame(all_results)

    # Agrupa por algoritmo e soma os hits (True = 1, False = 0)
    hits_por_algoritmo = df.groupby('algorithm')['is_hit'].sum()

    # Encontra o algoritmo com o maior número de hits
    best_algorithm_name = hits_por_algoritmo.idxmax()

    print("\n" + "=" * 50)
    print("ANÁLISE DE PERFORMANCE FINAL")
    print("=" * 50)
    print(f"Total de Hits por Algoritmo:\n{hits_por_algoritmo}")
    print(f"\nO melhor algoritmo foi: {best_algorithm_name}")

    # Salva o nome do melhor algoritmo em um arquivo de configuração
    try:
        with open("cache_config.txt", "w") as f:
            f.write(best_algorithm_name)
        print(f"Configuração salva: '{best_algorithm_name}' foi definido como o cache padrão.")
    except IOError as e:
        print(f"Erro ao salvar o arquivo de configuração: {e}")
    print("=" * 50)

def start_simulation_mode(reader_func):
    """Função principal que orquestra o modo de simulação."""
    algorithms_to_test = [FIFOCache, LRUCache, LFUCache]
    all_simulation_results = []

    for cache_class in algorithms_to_test:
        cache_instance = cache_class(capacity=10, reader_func=reader_func)
        results = run_single_simulation(cache_instance)
        all_simulation_results.extend(results)

    # Substitua a chamada da função de plotagem pela de relatório
    # ANTES: analyze_and_plot(all_simulation_results)
    # Gera os gráficos conforme solicitado no PDF
    analyze_and_plot(all_simulation_results)

    # Analisa e salva o melhor algoritmo para a próxima execução
    analyze_and_save_best_algorithm(all_simulation_results)

    print_text_report(all_simulation_results) 
    
def print_text_report(all_results: list):
    """
    Analisa os resultados da simulação e imprime um relatório em texto no terminal.
    """
    if not all_results:
        print("Nenhum resultado para gerar relatório.")
        return

    df = pd.DataFrame(all_results)
    
    print("\n\n" + "="*50)
    print("RELATÓRIO DE PERFORMANCE DA SIMULAÇÃO DE CACHE")
    print("="*50)

    # Agrupa os dados por algoritmo e por padrão de acesso
    grouped = df.groupby(['algorithm', 'pattern'])

    for (algorithm, pattern), group in grouped:
        total_hits = group['is_hit'].sum()
        total_misses = len(group) - total_hits
        total_accesses = len(group)
        hit_ratio = (total_hits / total_accesses) * 100 if total_accesses > 0 else 0
        avg_time = group['time'].mean()

        print(f"\n--- Algoritmo: {algorithm} | Padrão: {pattern} ---")
        print(f"  - Total de Acessos: {total_accesses}")
        print(f"  - Cache Hits:       {total_hits}")
        print(f"  - Cache Misses:     {total_misses}")
        print(f"  - Taxa de Acerto:   {hit_ratio:.2f}%")
        print(f"  - Tempo Médio de Acesso: {avg_time:.6f} segundos")

    print("\n" + "="*50)
    print("ANÁLISE DE TEXTOS COM MAIS CACHE MISSES")
    print("="*50)
    
    # Filtra apenas os misses e conta a ocorrência de cada text_id
    df_misses = df[df['is_hit'] == False]
    misses_per_text = df_misses['text_id'].value_counts().nlargest(10)

    if misses_per_text.empty:
        print("Nenhum cache miss foi registrado.")
    else:
        print("Top 10 textos que mais causaram cache miss no geral:")
        print(misses_per_text)
    
    print("="*50)