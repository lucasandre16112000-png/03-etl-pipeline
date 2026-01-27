# etl/loaders/data_loader.py

import pandas as pd
from pathlib import Path
from typing import Union, Optional
from ..config.logger import setup_logger
from ..config.settings import settings

logger = setup_logger(__name__)

class DataLoader:
    """Carregador de dados em múltiplos formatos - 100% compatível com Windows"""
    
    @staticmethod
    def load_csv(df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
        """
        Carregar dados em arquivo CSV
        
        Args:
            df: DataFrame
            file_path: Caminho do arquivo de saída
            **kwargs: Argumentos adicionais para to_csv
        """
        file_path = Path(file_path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Usar encoding utf-8 por padrão
            if 'encoding' not in kwargs:
                kwargs['encoding'] = 'utf-8'
            
            df.to_csv(file_path, index=False, **kwargs)
            logger.info(f"✓ Dados carregados em CSV: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {str(e)}")
            raise
    
    @staticmethod
    def load_json(df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
        """
        Carregar dados em arquivo JSON
        
        Args:
            df: DataFrame
            file_path: Caminho do arquivo de saída
            **kwargs: Argumentos adicionais para to_json
        """
        file_path = Path(file_path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_json(file_path, orient="records", **kwargs)
            logger.info(f"✓ Dados carregados em JSON: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar JSON: {str(e)}")
            raise
    
    @staticmethod
    def load_excel(df: pd.DataFrame, file_path: Union[str, Path], sheet_name: str = "Sheet1", **kwargs) -> None:
        """
        Carregar dados em arquivo Excel
        
        Args:
            df: DataFrame
            file_path: Caminho do arquivo de saída
            sheet_name: Nome da planilha
            **kwargs: Argumentos adicionais para to_excel
        """
        file_path = Path(file_path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_excel(file_path, sheet_name=sheet_name, index=False, **kwargs)
            logger.info(f"✓ Dados carregados em Excel: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar Excel: {str(e)}")
            raise
    
    @staticmethod
    def load_parquet(df: pd.DataFrame, file_path: Union[str, Path], **kwargs) -> None:
        """
        Carregar dados em arquivo Parquet
        
        Args:
            df: DataFrame
            file_path: Caminho do arquivo de saída
            **kwargs: Argumentos adicionais para to_parquet
        """
        file_path = Path(file_path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_parquet(file_path, index=False, **kwargs)
            logger.info(f"✓ Dados carregados em Parquet: {file_path}")
        except ImportError:
            logger.error("PyArrow não está instalado. Execute: pip install pyarrow")
            raise
        except Exception as e:
            logger.error(f"Erro ao carregar Parquet: {str(e)}")
            raise
    
    @classmethod
    def load(cls, df: pd.DataFrame, file_path: Union[str, Path], file_type: Optional[str] = None, **kwargs) -> None:
        """
        Carregar dados detectando o tipo automaticamente
        
        Args:
            df: DataFrame
            file_path: Caminho do arquivo de saída
            file_type: Tipo de arquivo (csv, json, excel, parquet). Se None, detecta pela extensão
            **kwargs: Argumentos adicionais
        """
        file_path = Path(file_path)
        
        if file_type is None:
            file_type = file_path.suffix.lower().lstrip(".")
        
        file_type = file_type.lower()
        
        if file_type == "csv":
            cls.load_csv(df, file_path, **kwargs)
        elif file_type == "json":
            cls.load_json(df, file_path, **kwargs)
        elif file_type in ["xlsx", "xls", "excel"]:
            cls.load_excel(df, file_path, **kwargs)
        elif file_type == "parquet":
            cls.load_parquet(df, file_path, **kwargs)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}. Suportados: {', '.join(settings.SUPPORTED_FORMATS)}")
