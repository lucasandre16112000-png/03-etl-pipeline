# etl/config/logger.py

import logging
import sys
from pathlib import Path
from .settings import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Configurar logger para um módulo específico - 100% compatível com Windows
    
    Args:
        name: Nome do módulo
        
    Returns:
        Logger configurado
    """
    try:
        settings.ensure_directories()
    except Exception as e:
        print(f"Aviso: Erro ao criar diretórios de log: {e}")
    
    logger = logging.getLogger(name)
    
    # Evitar adicionar handlers múltiplas vezes
    if logger.handlers:
        return logger
    
    try:
        logger.setLevel(settings.LOG_LEVEL)
    except ValueError:
        logger.setLevel("INFO")
    
    # Handler para console
    try:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(settings.LOG_LEVEL)
        console_formatter = logging.Formatter(settings.LOG_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        print(f"Aviso: Erro ao configurar handler de console: {e}")
    
    # Handler para arquivo - com tratamento especial para Windows
    try:
        log_file = settings.LOGS_DIR / f"{name.replace('.', '_')}.log"
        
        # Windows pode ter problemas com nomes de arquivo muito longos
        if len(str(log_file)) > 260:
            log_file = settings.LOGS_DIR / "pipeline.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(settings.LOG_LEVEL)
        file_formatter = logging.Formatter(settings.LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except PermissionError:
        print(f"Aviso: Sem permissão para criar arquivo de log. Continuando sem arquivo de log.")
    except Exception as e:
        print(f"Aviso: Erro ao configurar handler de arquivo: {e}")
    
    return logger
