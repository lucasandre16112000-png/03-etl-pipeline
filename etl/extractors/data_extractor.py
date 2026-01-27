# etl/extractors/data_extractor.py

import pandas as pd
from pathlib import Path
from typing import Union, Optional
from ..config.logger import setup_logger
from ..config.settings import settings

logger = setup_logger(__name__)

class DataExtractor:
    """Extrator de dados de múltiplas fontes - 100% compatível com Windows"""
    
    @staticmethod
    def extract_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Extrair dados de arquivo CSV
        
        Args:
            file_path: Caminho do arquivo
            **kwargs: Argumentos adicionais para pd.read_csv
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        logger.info(f"Extraindo dados de CSV: {file_path}")
        try:
            # Usar encoding utf-8 por padrão para melhor compatibilidade
            if 'encoding' not in kwargs:
                kwargs['encoding'] = 'utf-8'
            
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"✓ Extraído {len(df)} registros de {file_path}")
            return df
        except UnicodeDecodeError:
            # Tentar com latin-1 se utf-8 falhar
            logger.warning(f"Tentando encoding latin-1 para {file_path}")
            kwargs['encoding'] = 'latin-1'
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"✓ Extraído {len(df)} registros de {file_path} (encoding: latin-1)")
            return df
        except Exception as e:
            logger.error(f"Erro ao extrair CSV: {str(e)}")
            raise
    
    @staticmethod
    def extract_json(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Extrair dados de arquivo JSON
        
        Args:
            file_path: Caminho do arquivo
            **kwargs: Argumentos adicionais para pd.read_json
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        logger.info(f"Extraindo dados de JSON: {file_path}")
        try:
            df = pd.read_json(file_path, **kwargs)
            logger.info(f"✓ Extraído {len(df)} registros de {file_path}")
            return df
        except Exception as e:
            logger.error(f"Erro ao extrair JSON: {str(e)}")
            raise
    
    @staticmethod
    def extract_excel(file_path: Union[str, Path], sheet_name: int = 0, **kwargs) -> pd.DataFrame:
        """
        Extrair dados de arquivo Excel
        
        Args:
            file_path: Caminho do arquivo
            sheet_name: Nome ou índice da planilha
            **kwargs: Argumentos adicionais para pd.read_excel
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        logger.info(f"Extraindo dados de Excel: {file_path}")
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            logger.info(f"✓ Extraído {len(df)} registros de {file_path}")
            return df
        except Exception as e:
            logger.error(f"Erro ao extrair Excel: {str(e)}")
            raise
    
    @staticmethod
    def extract_parquet(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Extrair dados de arquivo Parquet
        
        Args:
            file_path: Caminho do arquivo
            **kwargs: Argumentos adicionais para pd.read_parquet
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        logger.info(f"Extraindo dados de Parquet: {file_path}")
        try:
            df = pd.read_parquet(file_path, **kwargs)
            logger.info(f"✓ Extraído {len(df)} registros de {file_path}")
            return df
        except ImportError:
            logger.error("PyArrow não está instalado. Execute: pip install pyarrow")
            raise
        except Exception as e:
            logger.error(f"Erro ao extrair Parquet: {str(e)}")
            raise
    
    @classmethod
    def extract(cls, file_path: Union[str, Path], file_type: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Extrair dados detectando o tipo automaticamente
        
        Args:
            file_path: Caminho do arquivo
            file_type: Tipo de arquivo (csv, json, excel, parquet). Se None, detecta pela extensão
            **kwargs: Argumentos adicionais
            
        Returns:
            DataFrame com os dados
        """
        file_path = Path(file_path)
        
        # Verificar se arquivo existe
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        if file_type is None:
            file_type = file_path.suffix.lower().lstrip(".")
        
        file_type = file_type.lower()
        
        if file_type == "csv":
            return cls.extract_csv(file_path, **kwargs)
        elif file_type == "json":
            return cls.extract_json(file_path, **kwargs)
        elif file_type in ["xlsx", "xls", "excel"]:
            return cls.extract_excel(file_path, **kwargs)
        elif file_type == "parquet":
            return cls.extract_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}. Suportados: {', '.join(settings.SUPPORTED_FORMATS)}")
