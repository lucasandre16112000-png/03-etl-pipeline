# etl/config/settings.py

import os
import sys
from pathlib import Path
from typing import Optional

class Settings:
    """Configurações do pipeline ETL - 100% compatível com Windows"""
    
    # Diretórios - Usando Path para compatibilidade cross-platform
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_INPUT_DIR = BASE_DIR / "data" / "input"
    DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Processamento
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    
    # Validação
    STRICT_MODE = os.getenv("STRICT_MODE", "False").lower() == "true"
    REMOVE_DUPLICATES = os.getenv("REMOVE_DUPLICATES", "True").lower() == "true"
    HANDLE_MISSING_VALUES = os.getenv("HANDLE_MISSING_VALUES", "True").lower() == "true"
    
    # Formatos suportados
    SUPPORTED_FORMATS = ["csv", "json", "excel", "parquet", "xlsx", "xls"]
    
    # Informações do Sistema
    IS_WINDOWS = sys.platform.startswith('win')
    IS_LINUX = sys.platform.startswith('linux')
    IS_MAC = sys.platform == 'darwin'
    
    @classmethod
    def ensure_directories(cls):
        """Garantir que todos os diretórios existem - compatível com Windows"""
        try:
            for directory in [cls.DATA_INPUT_DIR, cls.DATA_OUTPUT_DIR, cls.LOGS_DIR]:
                directory.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            # Tratamento especial para Windows com permissões
            import warnings
            warnings.warn(f"Aviso: Sem permissão para criar diretório {directory}. {str(e)}")
        except Exception as e:
            import warnings
            warnings.warn(f"Aviso: Erro ao criar diretório: {str(e)}")

settings = Settings()
