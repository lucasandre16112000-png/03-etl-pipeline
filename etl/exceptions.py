# etl/exceptions.py

"""
Exceções personalizadas para o Pipeline ETL
"""

class ETLException(Exception):
    """Exceção base para o pipeline ETL"""
    pass

class ExtractionError(ETLException):
    """Erro durante extração de dados"""
    pass

class TransformationError(ETLException):
    """Erro durante transformação de dados"""
    pass

class LoadingError(ETLException):
    """Erro durante carregamento de dados"""
    pass

class ValidationError(ETLException):
    """Erro durante validação de dados"""
    pass

class ConfigurationError(ETLException):
    """Erro de configuração"""
    pass

class FileNotFoundError(ETLException):
    """Arquivo não encontrado"""
    pass

class UnsupportedFormatError(ETLException):
    """Formato de arquivo não suportado"""
    pass
