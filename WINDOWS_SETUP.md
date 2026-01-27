# Guia de Instalação - Pipeline ETL no Windows

## ✅ Compatibilidade Garantida

Este projeto é **100% compatível com Windows 7, 8, 10 e 11**.

## 📋 Pré-requisitos

- **Windows 7 ou superior**
- **Python 3.9 ou superior** (recomendado: Python 3.11+)
- **Git** (opcional, para clonar o repositório)

## 🚀 Instalação Rápida

### Opção 1: Usando o Script Batch (Recomendado)

1. **Abra o Prompt de Comando (CMD)** ou **PowerShell**
2. **Navegue até o diretório do projeto:**
   ```cmd
   cd caminho\para\03-etl-pipeline
   ```

3. **Execute o script de exemplo:**
   ```cmd
   run_example.bat
   ```

   Ou para executar os testes:
   ```cmd
   run_tests.bat
   ```

O script cuidará de:
- ✅ Verificar se Python está instalado
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Executar o pipeline ou testes

### Opção 2: Instalação Manual

1. **Abra o Prompt de Comando (CMD)**

2. **Navegue até o diretório do projeto:**
   ```cmd
   cd caminho\para\03-etl-pipeline
   ```

3. **Crie um ambiente virtual:**
   ```cmd
   python -m venv venv
   ```

4. **Ative o ambiente virtual:**
   ```cmd
   venv\Scripts\activate.bat
   ```

   Você verá `(venv)` no início da linha de comando.

5. **Instale as dependências:**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Execute o exemplo:**
   ```cmd
   python example_usage.py
   ```

   Ou execute os testes:
   ```cmd
   pytest
   ```

## 🔍 Verificação de Instalação

Para verificar se tudo está funcionando corretamente:

```cmd
python -c "import pandas; import numpy; import openpyxl; print('✓ Todas as dependências instaladas com sucesso!')"
```

## 📁 Estrutura de Diretórios

Após a execução, você terá:

```
03-etl-pipeline/
├── venv/                          # Ambiente virtual (criado automaticamente)
├── data/
│   ├── input/                     # Dados de entrada
│   └── output/                    # Dados processados
├── logs/                          # Arquivos de log
├── etl/                           # Código principal
├── tests/                         # Testes
├── example_usage.py               # Exemplo de uso
├── run_example.bat                # Script para executar exemplo
├── run_tests.bat                  # Script para executar testes
└── requirements.txt               # Dependências
```

## 🐛 Solução de Problemas

### "Python não encontrado"
- Instale Python de https://www.python.org/downloads/
- **Importante:** Marque "Add Python to PATH" durante a instalação
- Reinicie o Prompt de Comando após instalar

### "Módulo não encontrado"
- Certifique-se de que o ambiente virtual está ativado (veja `(venv)` no prompt)
- Execute: `pip install -r requirements.txt`

### "Permissão negada" ao criar venv
- Execute o Prompt de Comando como Administrador
- Ou tente: `python -m venv venv --clear`

### Erro com encoding em arquivos CSV
- O projeto detecta automaticamente e tenta múltiplos encodings (UTF-8, Latin-1)
- Se persistir, edite o arquivo CSV com encoding UTF-8 no Notepad++

### Erro com PyArrow (Parquet)
- PyArrow é instalado automaticamente
- Se tiver problemas, execute: `pip install --upgrade pyarrow`

## 📊 Executando o Pipeline

### Exemplo Básico

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
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
    .remove_duplicates(subset=['email']) \
    .handle_missing_values(strategy="fill", fill_value=0) \
    .rename_columns({'id': 'customer_id'}) \
    .filter_rows(lambda df: df['age'] > 18) \
    .convert_types({'age': 'int', 'salary': 'float'}) \
    .add_column('age_group', lambda row: 'Senior' if row['age'] >= 60 else 'Adult') \
    .load("data/output/resultado.csv") \
    .load("data/output/resultado.json") \
    .load("data/output/resultado.xlsx")

pipeline.finish(execution_time=5.2)
pipeline.save_stats("data/output/stats.json")
```

## 🧪 Executando Testes

### Todos os testes:
```cmd
pytest
```

### Testes com cobertura:
```cmd
pytest --cov=etl
```

### Teste específico:
```cmd
pytest tests/test_pipeline.py::TestETLPipeline::test_extract
```

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (ou copie `.env.example`):

```
LOG_LEVEL=INFO
BATCH_SIZE=1000
MAX_WORKERS=4
STRICT_MODE=False
REMOVE_DUPLICATES=True
HANDLE_MISSING_VALUES=True
```

## 🎯 Formatos Suportados

- **Entrada:** CSV, JSON, Excel (.xlsx, .xls), Parquet
- **Saída:** CSV, JSON, Excel (.xlsx), Parquet

## 💡 Dicas

1. **Use caminhos relativos** para melhor portabilidade
2. **Sempre ative o venv** antes de trabalhar com o projeto
3. **Verifique os logs** em `logs/` se algo der errado
4. **Use UTF-8** para arquivos CSV quando possível

## 🔗 Links Úteis

- [Python Downloads](https://www.python.org/downloads/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Pytest Documentation](https://docs.pytest.org/)

## ✅ Tudo Pronto!

Seu ambiente está 100% configurado para Windows. Bom trabalho! 🚀
