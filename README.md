# 🔄 App 3: Pipeline ETL Profissional com Pandas

Este projeto é uma demonstração completa de um pipeline de **Extração, Transformação e Carga (ETL)**, construído inteiramente com **Python** e **Pandas**. Ele simula um cenário real de engenharia de dados, onde dados brutos são coletados, limpos, validados, transformados e, finalmente, carregados em um formato pronto para análise.

## ✨ Funcionalidades Principais

- **Extração (Extract)**: Capacidade de ler dados de múltiplas fontes, como CSV, JSON e Excel.
- **Limpeza de Dados (Clean)**: Remove registros duplicados e trata valores ausentes (`NaN`).
- **Validação de Dados (Validate)**: Verifica a integridade dos dados, como formatos de e-mail e telefone.
- **Transformação (Transform)**: Enriquece os dados brutos, criando novas colunas derivadas.
- **Carga (Load)**: Salva os dados processados em múltiplos formatos (CSV e JSON).

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
| :--- | :--- | :--- |
| **Python** | 3.11+ | Linguagem principal |
| **Pandas** | 2.1.3 | Manipulação e análise de dados em alta performance |
| **NumPy** | 1.26.2 | Computação numérica e geração de dados |

## 📋 Guia de Instalação e Execução (Para Qualquer Pessoa)

### Pré-requisitos

1.  **Git**: [**Download aqui**](https://git-scm.com/downloads)
2.  **Python**: [**Download aqui**](https://www.python.org/downloads/) (versão 3.8+)

### Passo 1: Baixar o Projeto

```bash
git clone https://github.com/lucasandre16112000-png/03-etl-pipeline.git
cd 03-etl-pipeline
```

### Passo 2: Criar e Ativar um Ambiente Virtual

```bash
# No Windows
python -m venv venv
.\venv\Scripts\activate

# No macOS ou Linux
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar as Bibliotecas

```bash
pip install -r requirements.txt
```

### Passo 4: Executar o Pipeline

```bash
python pipeline.py
```

### Passo 5: Verificar os Resultados

- O terminal mostrará as estatísticas do processo.
- Três arquivos serão criados na pasta:
    - `processed_data.csv`
    - `processed_data.json`
    - `pipeline_statistics.json`

## 🤔 Solução de Problemas Comuns

- **`ModuleNotFoundError: No module named 'pandas'`**: Certifique-se de que o ambiente virtual (venv) está ativado (Passo 2) e que você instalou as dependências (Passo 3).

## 👨‍💻 Autor

Lucas André S - [GitHub](https://github.com/lucasandre16112000-png)
