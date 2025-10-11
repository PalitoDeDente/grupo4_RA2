import time
import os

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
    print("Cache ainda não implementado. Todas as chamadas irão direto ao disco.")

    while True:
        try:
            user_input = input("Digite o número do texto (1-100), -1 para  simulação ou 0 para sair: ")
            text_id = int(user_input)

            if text_id == 0:
                print("Encerrando...")
                break
            elif text_id == -1:
                run_simulation()
            elif 1 <= text_id <= 100:
                start_time = time.time()
                # Lógica de acesso (deve ser substituída pela chamada ao cache, aqui vai pegar direto)
                content = read_from_slow_disk(text_id)
                end_time = time.time()

                print("\n--- Conteúdo do Texto ---")
                print(content[:500] + "..." if len(content) > 500 else content) # é pra mostrar um trecho apenas
                print("--------------------------------")
                print(f"Tempo de carregamento: {end_time - start_time:.4f} segundos. \n")
            else:
                print("Entrada inválida. Por favor, digite um número entre 1 e 100 para leitura dos textos, -1 para simulação e 0 para encerrar o programa.\n")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número. ")

if __name__ == "__main__":
    main()

