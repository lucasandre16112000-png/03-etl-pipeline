@echo off
REM Script para executar o exemplo do Pipeline ETL no Windows
REM Compatível com Windows 7+

setlocal enabledelayedexpansion

REM Cores no Windows (usando modo de compatibilidade)
cls
echo.
echo ============================================
echo Pipeline ETL - Windows Launcher
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
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
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
        echo.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado com sucesso.
    echo.
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    echo.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado.
echo.

REM Upgrade pip
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [AVISO] Falha ao atualizar pip, continuando mesmo assim...
    echo.
)

REM Instalar dependências
echo [INFO] Instalando dependências...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependências!
    echo.
    pause
    exit /b 1
)
echo [OK] Dependências instaladas com sucesso.
echo.

REM Executar exemplo
echo [INFO] Executando pipeline...
echo.
echo ============================================
echo.
python example_usage.py
set exit_code=%errorlevel%

echo.
echo ============================================
echo.

if %exit_code% equ 0 (
    echo [SUCESSO] Pipeline executado com sucesso!
    echo.
    echo Arquivos de saida:
    echo - data\output\processed_data.csv
    echo - data\output\processed_data.json
    echo - data\output\processed_data.xlsx
    echo - data\output\pipeline_stats.json
    echo.
    echo Logs disponíveis em: logs\
    echo.
) else (
    echo [ERRO] Pipeline falhou com codigo: %exit_code%
    echo.
    echo Verifique os logs em: logs\
    echo.
)

pause
exit /b %exit_code%
