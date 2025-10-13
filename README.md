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