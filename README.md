# Projeto de Algoritmos de Cache - RA2

## 📝 Descrição do Projeto

Este projeto foi desenvolvido como atividade avaliativa para a disciplina de Sistemas Operacionais. O objetivo é criar um aplicativo de terminal para a leitura de textos que minimiza o tempo de carregamento de arquivos armazenados em um disco lento simulado. Para alcançar a eficiência, o sistema utiliza uma estrutura de cache em memória capaz de armazenar até 10 textos.

A aplicação implementa e compara o desempenho de três algoritmos de substituição de cache (FIFO, LRU e LFU) através de um robusto modo de simulação. O objetivo final é analisar os dados de performance e indicar qual algoritmo é o mais eficiente para o cenário proposto pela empresa "Texto é Vida".

## 👥 Equipe e Divisão de Tarefas

* **Aluno A - Ricardo Hey (Coordenador):**
    * Implementação da estrutura base do projeto e leitura do disco lento.
    * Desenvolvimento do laço principal da aplicação e interface com o usuário.
    * Criação da interface abstrata (`Cache`) para acoplar os algoritmos.
    * Coordenação do repositório e integração dos módulos.

* **Aluno B - Eduardo Rodrigues Araujo de Oliveira:**
    * Projeto e implementação da estrutura de dados principal do cache (`BaseCache`).
    * Implementação do primeiro algoritmo de substituição: **FIFO** (First-In, First-Out).
    * Integração e medição de performance do algoritmo FIFO.

* **Aluno C -  Ricardo Hey:**
    * Implementação do segundo algoritmo de substituição: **LRU** (Least Recently Used).
    * Integração e testes para validar a lógica e a performance do LRU.
    * Implementação de um quarto algoritmo de substituição: **ARC** (Adaptive Replacement Cache).

* **Aluno D - Eduardo Rodrigues Araujo de Oliveira:**
    * Implementação do terceiro algoritmo de substituição: **LFU** (Least Frequently Used).
    * Desenvolvimento completo do **Modo de Simulação**, incluindo a lógica de usuários, padrões de sorteio e coleta de dados.
    * Geração dos gráficos e do relatório final para análise comparativa.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Controle de Versão:** Git e GitHub
* **Bibliotecas Principais:**
    * `numpy`
    * `pandas`
    * `matplotlib`
    * `seaborn`

## 🚀 Como Executar o Projeto

### Pré-requisitos

* Python 3.10+
* Git

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/PalitoDeDente/grupo4_RA2.git
    cd grupo4_RA2
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv .meu_ambiente
    source .meu_ambiente/bin/activate  # No Linux/macOS
    # .\.meu_ambiente\Scripts\activate    # No Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Estrutura de Textos:**
    Certifique-se de que a pasta `/texts` existe na raiz do projeto e contém 100 arquivos de texto (`1.txt`, `2.txt`, ..., `100.txt`).

### Execução

Para rodar o programa, execute o arquivo principal a partir da raiz do projeto:

```bash
python ra2_main.py
```

**Comandos disponíveis no terminal:**
* **`1` a `100`:** Solicita um texto. O sistema mostrará se foi um *Cache Hit* (rápido) ou *Cache Miss* (lento).
* **`-1`:** Inicia o **Modo de Simulação**. Os gráficos e relatórios serão gerados ao final.
* **`0`:** Encerra a aplicação.

## 🧠 Fundamentos Teóricos

Esta seção detalha os conceitos centrais por trás do funcionamento do projeto.

### Cache Rápido vs. Disco Lento

O princípio fundamental deste projeto é a hierarquia de memória. No nosso sistema:
* **O Disco Lento:** É simulado pela leitura dos arquivos na pasta `/texts/`. Adicionamos um atraso artificial (`time.sleep`) a essa leitura para emular a lentidão de um sistema de armazenamento físico, como um disco rígido ou um acesso remoto. Toda vez que ocorre um **"Cache Miss"**, somos forçados a acessar este meio lento.
* **O Cache Rápido:** É simulado pelas estruturas de dados que implementamos em memória (dicionários, listas, etc.). Este cache tem um tamanho limitado (10 textos) e armazena os textos mais relevantes. O acesso à memória RAM é ordens de magnitude mais rápido que o acesso ao disco. Um **"Cache Hit"** significa que encontramos o texto aqui, resultando em um carregamento quase instantâneo para o usuário.

O objetivo de um algoritmo de cache é gerenciar de forma inteligente o espaço limitado do cache rápido para maximizar o número de *hits* e minimizar o número de *misses*.

### Algoritmos de Substituição Implementados

Quando o cache está cheio e um novo texto precisa ser adicionado (após um *miss*), um texto existente deve ser removido. Esse processo é chamado de **evicção**. Cada algoritmo implementa uma política de evicção diferente:

* **FIFO (First-In, First-Out):** É o algoritmo mais simples. Ele se comporta como uma fila. O primeiro texto que foi adicionado ao cache é o primeiro a ser removido, independentemente de quantas vezes ou quão recentemente ele foi acessado.
* **LRU (Least Recently Used):** Este algoritmo remove o texto que não é acessado há mais tempo. A lógica é que, se um texto não foi usado recentemente, é provável que não seja usado novamente no futuro próximo. Ele mantém os textos "quentes" (usados recentemente) no cache.
* **LFU (Least Frequently Used):** Remove o texto que foi acessado o menor número de vezes. A ideia é que textos "populares" (com alta frequência de acesso) são mais importantes de se manter no cache, mesmo que não tenham sido acessados muito recentemente.
* **ARC (Adaptive Replacement Cache):** Um algoritmo mais avançado, o ARC é adaptativo: ele gerencia duas listas, uma com itens acessados recentemente (estilo LRU) e outra com itens acessados frequentemente (estilo LFU). Ele ajusta dinamicamente o tamanho dessas listas com base no padrão de acesso, tentando obter o melhor dos dois mundos e se adaptar a diferentes tipos de carga de trabalho.

### O Modo de Simulação

Para comparar os algoritmos de forma justa, o **Modo de Simulação** executa um teste automatizado e intensivo. Ele funciona da seguinte forma:
1.  **Simulação de Usuários:** Simula 3 usuários distintos para cada algoritmo.
2.  **Volume de Requisições:** Cada usuário faz 200 solicitações de textos, totalizando 600 requisições por algoritmo.
3.  **Padrões de Acesso:** As solicitações são geradas seguindo três padrões distintos para testar a resiliência dos algoritmos:
    * **Aleatório Puro:** Qualquer texto de 1 a 100 tem a mesma chance de ser escolhido.
    * **Distribuição de Poisson:** Um padrão que tende a concentrar os acessos em torno de uma média, simulando um "pico" de interesse em certos textos.
    * **Ponderado:** Simula um cenário realista onde um grupo específico de textos (30 a 40) é muito mais popular, tendo 43% de chance de ser escolhido.

## Análise dos Resultados da Simulação

*Adicionar aqui uma analise breve de cada um dos algoritmos testados na simulação*
