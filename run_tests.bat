@echo off
REM Script para executar testes do Pipeline ETL no Windows
REM Compatível com Windows 7+

setlocal enabledelayedexpansion

cls
echo.
echo ============================================
echo Pipeline ETL - Test Runner (Windows)
echo ============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.9 ou superior:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python encontrado:
python --version
echo.

REM Verificar se venv existe, se não, criar
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado.
echo.

REM Instalar dependências
echo [INFO] Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências!
    pause
    exit /b 1
)
echo [OK] Dependências instaladas.
echo.

REM Executar testes
echo [INFO] Executando testes com pytest...
echo.
echo ============================================
echo.
pytest -v --tb=short
set exit_code=%errorlevel%

echo.
echo ============================================
echo.

if %exit_code% equ 0 (
    echo [SUCESSO] Todos os testes passaram!
) else (
    echo [ERRO] Alguns testes falharam com codigo: %exit_code%
)

echo.
pause
exit /b %exit_code%
