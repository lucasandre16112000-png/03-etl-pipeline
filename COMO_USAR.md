# Como Usar o Pipeline ETL - Guia Prático

Um guia passo a passo para usar o Pipeline ETL, desde a instalação até o processamento de seus próprios dados.

---

## 📋 Índice

1. [Instalação Rápida](#instalação-rápida)
2. [Executar o Exemplo](#executar-o-exemplo)
3. [Usar com Seus Dados](#usar-com-seus-dados)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Perguntas Frequentes](#perguntas-frequentes)

---

## 🚀 Instalação Rápida

### Passo 1: Baixar o Projeto

**Opção A: Com Git (Recomendado)**

1. Abra o **Prompt de Comando (CMD)** ou **PowerShell**
2. Cole este comando:
   ```cmd
   git clone https://github.com/lucasandre16112000-png/03-etl-pipeline.git
   ```
3. Pressione Enter e aguarde

**Opção B: Sem Git**

1. Acesse: https://github.com/lucasandre16112000-png/03-etl-pipeline
2. Clique em **Code** → **Download ZIP**
3. Extraia a pasta em um local de sua preferência
4. Abra o **Prompt de Comando** e navegue até a pasta:
   ```cmd
   cd C:\caminho\para\03-etl-pipeline
   ```

### Passo 2: Entrar na Pasta do Projeto

```cmd
cd 03-etl-pipeline
```

### Passo 3: Verificar se Python está Instalado

```cmd
python --version
```

Se aparecer um número de versão (ex: Python 3.12.0), está tudo certo! ✅

Se não funcionar, [instale Python aqui](https://www.python.org/downloads/)

---

## 🎯 Executar o Exemplo

### Windows - Opção 1: Usando o Script (Mais Fácil)

```cmd
run_example.bat
```

Isso é tudo! O script faz tudo automaticamente.

### Windows - Opção 2: Usando CMD (Prompt de Comando)

1. Abra o **Prompt de Comando (CMD)**
   - Pressione `Win + R`
   - Digite `cmd`
   - Pressione Enter

2. Navegue até a pasta do projeto:
   ```cmd
   cd C:\Users\SeuUsuario\03-etl-pipeline
   ```
   
   (Substitua `C:\Users\SeuUsuario` pelo caminho real da sua pasta)

3. Crie o ambiente virtual:
   ```cmd
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   Você verá `(venv)` no início da linha - isso significa que está ativado ✅

5. Instale as dependências:
   ```cmd
   pip install -r requirements.txt
   ```

6. Execute o exemplo:
   ```cmd
   python example_usage.py
   ```

7. Quando terminar, desative o ambiente:
   ```cmd
   deactivate
   ```

### Windows - Opção 3: Usando PowerShell

1. Abra o **PowerShell**
   - Pressione `Win + X`
   - Clique em "Windows PowerShell"
   - Ou procure por "PowerShell" no menu Iniciar

2. Navegue até a pasta do projeto:
   ```powershell
   cd C:\Users\SeuUsuario\03-etl-pipeline
   ```

3. Crie o ambiente virtual:
   ```powershell
   python -m venv venv
   ```

4. Ative o ambiente virtual:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   Se receber erro de permissão, execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   
   Depois tente novamente:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

6. Execute o exemplo:
   ```powershell
   python example_usage.py
   ```

7. Quando terminar, desative o ambiente:
   ```powershell
   deactivate
   ```

### Linux/Mac

```bash
chmod +x run_example.sh
./run_example.sh
```

**O que acontece:**
- ✅ Cria um ambiente virtual
- ✅ Instala as dependências
- ✅ Processa dados de exemplo
- ✅ Gera arquivos de saída em `data/output/`

**Tempo estimado:** 2-3 minutos na primeira execução

---

## 📊 Usar com Seus Dados

### Passo 1: Preparar Seus Dados

1. Coloque seu arquivo CSV, JSON ou Excel em:
   ```
   data/input/
   ```

2. Seu arquivo pode ter qualquer nome, exemplo:
   - `clientes.csv`
   - `vendas.json`
   - `produtos.xlsx`

### Passo 2: Criar um Script Python

Crie um arquivo chamado `processar_meus_dados.py` na raiz do projeto:

```python
from etl.pipeline import ETLPipeline

# Criar pipeline
pipeline = ETLPipeline()
pipeline.run()

# Processar dados
pipeline.extract("data/input/clientes.csv") \
    .remove_duplicates() \
    .handle_missing_values(strategy="drop") \
    .load("data/output/clientes_processados.csv")

pipeline.finish()
```

### Passo 3: Executar

```cmd
python processar_meus_dados.py
```

### Passo 4: Verificar Resultados

Os dados processados estarão em:
```
data/output/clientes_processados.csv
```

---

## 💡 Exemplos Práticos

### Exemplo 1: Limpeza Básica de Dados

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

pipeline.extract("data/input/dados_brutos.csv") \
    .remove_duplicates() \
    .handle_missing_values(strategy="drop") \
    .load("data/output/dados_limpos.csv")

pipeline.finish()
```

**O que faz:**
- Remove linhas duplicadas
- Remove linhas com valores faltantes
- Salva em CSV

---

### Exemplo 2: Transformação de Dados

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

pipeline.extract("data/input/clientes.csv") \
    .rename_columns({
        "id": "cliente_id",
        "name": "nome_cliente",
        "email": "email_cliente"
    }) \
    .filter_rows(lambda df: df["idade"] > 18) \
    .convert_types({"idade": "int", "salario": "float"}) \
    .load("data/output/clientes_transformados.csv")

pipeline.finish()
```

**O que faz:**
- Renomeia colunas
- Filtra apenas maiores de 18 anos
- Converte tipos de dados
- Salva resultado

---

### Exemplo 3: Adicionar Colunas Calculadas

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

pipeline.extract("data/input/vendas.csv") \
    .add_column("categoria_valor", 
                lambda row: "Alto" if row["valor"] > 1000 else "Baixo") \
    .add_column("mes", 
                lambda row: row["data"].split("-")[1]) \
    .load("data/output/vendas_categorizado.csv") \
    .load("data/output/vendas_categorizado.json") \
    .load("data/output/vendas_categorizado.xlsx")

pipeline.finish()
```

**O que faz:**
- Cria coluna "categoria_valor" baseada no valor
- Extrai o mês da data
- Salva em 3 formatos diferentes

---

### Exemplo 4: Pipeline Completo

```python
from etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
pipeline.run()

# Pipeline completo com todas as transformações
pipeline.extract("data/input/dados_completos.csv") \
    .remove_duplicates(subset=["email"]) \
    .handle_missing_values(strategy="fill", fill_value=0) \
    .rename_columns({
        "id": "cliente_id",
        "name": "nome",
        "age": "idade"
    }) \
    .filter_rows(lambda df: df["idade"] >= 18) \
    .convert_types({
        "idade": "int",
        "salario": "float",
        "data_cadastro": "datetime"
    }) \
    .add_column("faixa_etaria", 
                lambda row: "Jovem" if row["idade"] < 30 else "Adulto") \
    .add_column("categoria_salario",
                lambda row: "Alto" if row["salario"] > 5000 else "Médio") \
    .load("data/output/dados_processados.csv") \
    .load("data/output/dados_processados.json") \
    .load("data/output/dados_processados.xlsx")

# Salvar estatísticas
pipeline.finish()
pipeline.save_stats("data/output/estatisticas.json")
```

**O que faz:**
- Remove duplicatas por email
- Preenche valores faltantes com 0
- Renomeia colunas
- Filtra maiores de 18 anos
- Converte tipos de dados
- Adiciona 2 colunas calculadas
- Salva em 3 formatos
- Gera relatório de estatísticas

---

## ❓ Perguntas Frequentes

### P: Como adiciono meus dados?

**R:** Coloque seus arquivos em `data/input/` e use:
```python
pipeline.extract("data/input/seu_arquivo.csv")
```

---

### P: Quais formatos são suportados?

**R:** Entrada: CSV, JSON, Excel, Parquet
Saída: CSV, JSON, Excel, Parquet

---

### P: Como faço para renomear colunas?

**R:** Use `rename_columns()`:
```python
.rename_columns({
    "coluna_antiga": "coluna_nova",
    "id": "cliente_id"
})
```

---

### P: Como filtro dados?

**R:** Use `filter_rows()` com uma função:
```python
.filter_rows(lambda df: df["idade"] > 18)
.filter_rows(lambda df: df["salario"] > 1000)
```

---

### P: Como adiciono colunas novas?

**R:** Use `add_column()`:
```python
.add_column("nova_coluna", lambda row: row["coluna1"] + row["coluna2"])
```

---

### P: Como salvo em vários formatos?

**R:** Use `.load()` múltiplas vezes:
```python
.load("data/output/resultado.csv") \
.load("data/output/resultado.json") \
.load("data/output/resultado.xlsx")
```

---

### P: Como removo linhas com valores faltantes?

**R:** Use `handle_missing_values()`:
```python
.handle_missing_values(strategy="drop")
```

---

### P: Como preencho valores faltantes com um valor?

**R:**
```python
.handle_missing_values(strategy="fill", fill_value=0)
```

---

### P: Como converto tipos de dados?

**R:** Use `convert_types()`:
```python
.convert_types({
    "idade": "int",
    "salario": "float",
    "data": "datetime"
})
```

---

### P: Como removo duplicatas?

**R:** Use `remove_duplicates()`:
```python
.remove_duplicates()  # Remove todas as duplicatas
.remove_duplicates(subset=["email"])  # Remove duplicatas por email
```

---

### P: Como vejo os logs?

**R:** Os logs são salvos em `logs/` automaticamente. Você também verá no terminal enquanto o script roda.

---

### P: Como vejo as estatísticas?

**R:** Após rodar o pipeline, verifique `data/output/pipeline_stats.json`

---

## 🧪 Executar os Testes

Para verificar se tudo está funcionando:

**Windows - Opção 1 (Mais Fácil):**
```cmd
run_tests.bat
```

**Windows - Opção 2 (CMD):**
```cmd
python -m pytest
```

**Windows - Opção 3 (PowerShell):**
```powershell
python -m pytest
```

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

Todos os testes devem passar ✅

---

## 📞 Precisa de Ajuda?

1. Verifique a seção de [Perguntas Frequentes](#perguntas-frequentes)
2. Veja o arquivo `example_usage.py` para mais exemplos
3. Consulte `README.md` para documentação completa
4. Consulte `README_EN.md` para versão em inglês

---

## 🎉 Pronto!

Agora você sabe como usar o Pipeline ETL! Comece com o exemplo e depois adapte para seus dados.

**Boa sorte! 🚀**

---

## 🔧 Troubleshooting - Problemas Comuns

### Problema: "Python não encontrado"

**Solução:**
1. Instale Python: https://www.python.org/downloads/
2. IMPORTANTE: Marque "Add Python to PATH" durante a instalação
3. Reinicie o computador
4. Tente novamente

---

### Problema: "pip não encontrado" (CMD)

**Solução 1:**
```cmd
python -m pip install -r requirements.txt
```

**Solução 2:**
- Desinstale Python
- Reinstale marcando "Add Python to PATH"
- Reinicie o computador

---

### Problema: "pip não encontrado" (PowerShell)

**Solução:**
```powershell
python -m pip install -r requirements.txt
```

---

### Problema: "Erro de permissão" (PowerShell)

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Digite Y e pressione Enter quando perguntado.

---

### Problema: "Módulo não encontrado"

**Solução:**
1. Certifique-se de que está na pasta correta
2. Certifique-se de que o venv está ativado (deve ver (venv) no prompt)
3. Instale as dependências novamente:
   ```cmd
   pip install -r requirements.txt
   ```

---

### Problema: "venv não funciona" (PowerShell)

**Solução:**
1. Execute como Administrador
2. Execute:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Tente ativar o venv novamente:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

---

### Problema: "Script não roda"

**Solução 1 (CMD):**
```cmd
python example_usage.py
```

**Solução 2 (PowerShell):**
```powershell
python example_usage.py
```

**Solução 3 (Executar como Administrador):**
- Clique com botão direito em CMD ou PowerShell
- Selecione "Run as Administrator"
- Tente novamente

