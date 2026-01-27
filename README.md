# Pipeline ETL Profissional - 100% Compatível com Windows

Um pipeline ETL (Extract, Transform, Load) de nível enterprise para processamento e transformação de dados, construído com Python e as melhores práticas de data engineering. **Totalmente compatível com Windows, Linux e macOS.**

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.1.3-blue.svg)](https://pandas.pydata.org/)
[![Pytest](https://img.shields.io/badge/pytest-7.4.3-blue.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Visão Geral

Este projeto implementa um pipeline ETL robusto e profissional que permite:

- **Extrair** dados de múltiplos formatos (CSV, JSON, Excel, Parquet)
- **Transformar** dados com operações complexas e encadeadas
- **Carregar** resultados em diferentes formatos
- **Validar** dados em cada etapa
- **Registrar** todas as operações com logging avançado
- **Monitorar** performance com estatísticas detalhadas

## ✨ Features Principais

| Categoria | Feature | Descrição |
|---|---|---|
| **Extração** | Suporte a Múltiplos Formatos | CSV, JSON, Excel, Parquet |
| | Detecção Automática | Identifica tipo de arquivo pela extensão |
| | Tratamento de Encoding | Suporte a UTF-8 e Latin-1 para CSV |
| **Transformação** | 9 Operações | Duplicatas, valores faltantes, renomeação, seleção, filtro, conversão, normalização, colunas calculadas, agregação |
| | Fluent API | Encadeamento de métodos para legibilidade |
| **Validação** | 7 Tipos de Validação | Email, telefone, numérico, data, string, lista, schema |
| **Carregamento** | Múltiplos Formatos | CSV, JSON, Excel, Parquet |
| **Operações** | Logging Estruturado | Rastreamento completo de operações |
| | Estatísticas Detalhadas | Métricas de performance e processamento |
| | Configuração por Ambiente | Suporte a `.env` para diferentes ambientes |
| **Compatibilidade** | **100% Windows** | Scripts `.bat` e código adaptado para Windows |
| | Cross-Platform | Funciona em Windows, Linux e macOS |

## 🚀 Começando

### Pré-requisitos

- **Python 3.9 ou superior**
- **Git** (opcional, para clonar)

### 1. Obtenha o Projeto

**Opção A: Clone com Git**
```bash
git clone https://github.com/lucasandre16112000-png/03-etl-pipeline.git
cd 03-etl-pipeline
```

**Opção B: Baixe o ZIP**
- Baixe e extraia o ZIP do projeto.
- Abra o terminal (CMD ou PowerShell) e navegue até a pasta.

### 2. Execute o Script de Setup

**No Windows:**
```cmd
run_example.bat
```

**No Linux/macOS:**
```bash
chmod +x run_example.sh
./run_example.sh
```

O script irá automaticamente:
- ✅ Criar um ambiente virtual (`venv`)
- ✅ Instalar todas as dependências
- ✅ Executar o pipeline de exemplo

## 📖 Uso

### Exemplo Básico

```python
from etl.pipeline import ETLPipeline

# Criar pipeline
pipeline = ETLPipeline()

# Executar transformações
pipeline.extract("data/input/seu_arquivo.csv") \
    .remove_duplicates() \
    .handle_missing_values(strategy="drop") \
    .load("data/output/resultado.csv")
```

### Exemplo Avançado

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

pipeline.extract("data/input/dados.csv") \
    .remove_duplicates(subset=["email"]) \
    .handle_missing_values(strategy="fill", fill_value=0) \
    .rename_columns({"id": "customer_id"}) \
    .filter_rows(lambda df: df["age"] > 18) \
    .convert_types({"age": "int", "salary": "float"}) \
    .add_column("age_group", lambda row: "Senior" if row["age"] >= 60 else "Adult") \
    .load("data/output/resultado.csv") \
    .load("data/output/resultado.json") \
    .load("data/output/resultado.xlsx")

pipeline.finish(execution_time=5.2)
pipeline.save_stats("data/output/stats.json")
```

## 🧪 Testes

Para executar todos os testes:

**No Windows:**
```cmd
run_tests.bat
```

**No Linux/macOS:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

## 📂 Estrutura do Projeto

```
03-etl-pipeline/
├── venv/                          # Ambiente virtual (criado automaticamente)
├── data/
│   ├── input/                     # Dados de entrada
│   └── output/                    # Dados processados
├── logs/                          # Arquivos de log
├── etl/                           # Código principal
│   ├── config/                    # Configurações
│   ├── extractors/                # Extratores de dados
│   ├── loaders/                   # Carregadores de dados
│   ├── transformers/              # Transformadores de dados
│   ├── validators/                # Validadores de dados
│   ├── exceptions.py              # Exceções personalizadas
│   ├── pipeline.py                # Pipeline principal
│   └── profiler.py                # Monitor de performance
├── tests/                         # Testes
├── .env.example                   # Exemplo de variáveis de ambiente
├── .gitignore
├── example_usage.py               # Exemplo de uso
├── requirements.txt               # Dependências
├── run_example.bat                # Script para Windows
├── run_example.sh                 # Script para Linux/Mac
├── run_tests.bat                  # Script de testes para Windows
├── run_tests.sh                   # Script de testes para Linux/Mac
├── WINDOWS_SETUP.md               # Guia de instalação para Windows
└── README.md                      # Este arquivo
```

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto (copie de `.env.example`) para configurar:

```
LOG_LEVEL=INFO
BATCH_SIZE=1000
MAX_WORKERS=4
STRICT_MODE=False
REMOVE_DUPLICATES=True
HANDLE_MISSING_VALUES=True
```

## 🎓 Boas Práticas Implementadas

1. **Arquitetura Modular**: Separação clara de responsabilidades
2. **Encadeamento de Métodos**: Fluent API para melhor legibilidade
3. **Logging Estruturado**: Rastreamento completo de operações
4. **Testes Abrangentes**: Cobertura de todos os módulos
5. **Documentação**: Docstrings e exemplos claros
6. **Configuração por Ambiente**: Suporte a diferentes ambientes
7. **Tratamento de Erros**: Exceções bem definidas
8. **Performance**: Operações otimizadas com pandas
9. **Compatibilidade Cross-Platform**: Código e scripts para Windows, Linux e macOS

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

Lucas André S - [GitHub](https://github.com/lucasandre16112000-png)

---

**Melhorado e tornado 100% compatível com Windows por Manus AI**
