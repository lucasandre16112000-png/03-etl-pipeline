# etl/transformers/data_transformer.py

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Callable
from ..config.logger import setup_logger
from ..config.settings import settings

logger = setup_logger(__name__)

class DataTransformer:
    """Transformador de dados profissional - 100% compatível com Windows"""
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = "first") -> pd.DataFrame:
        """
        Remover registros duplicados
        
        Args:
            df: DataFrame
            subset: Colunas para considerar na duplicação
            keep: Qual duplicata manter ('first', 'last', False)
            
        Returns:
            DataFrame sem duplicatas
        """
        try:
            initial_count = len(df)
            df = df.drop_duplicates(subset=subset, keep=keep)
            removed = initial_count - len(df)
            logger.info(f"✓ Removidas {removed} duplicatas")
            return df
        except Exception as e:
            logger.error(f"Erro ao remover duplicatas: {str(e)}")
            raise
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = "drop", fill_value: Any = None) -> pd.DataFrame:
        """
        Lidar com valores faltantes
        
        Args:
            df: DataFrame
            strategy: 'drop', 'fill', 'forward_fill', 'backward_fill'
            fill_value: Valor para preencher (se strategy='fill')
            
        Returns:
            DataFrame sem valores faltantes
        """
        try:
            missing_count = df.isnull().sum().sum()
            
            if missing_count == 0:
                logger.info("✓ Nenhum valor faltante encontrado")
                return df
            
            if strategy == "drop":
                df = df.dropna()
                logger.info(f"✓ Removidas {missing_count} linhas com valores faltantes")
            elif strategy == "fill":
                df = df.fillna(fill_value)
                logger.info(f"✓ Preenchidas {missing_count} valores faltantes com {fill_value}")
            elif strategy == "forward_fill":
                # Usar ffill() em vez de fillna(method='ffill') - compatível com pandas 2.0+
                df = df.ffill()
                logger.info(f"✓ Preenchidas {missing_count} valores faltantes (forward fill)")
            elif strategy == "backward_fill":
                # Usar bfill() em vez de fillna(method='bfill') - compatível com pandas 2.0+
                df = df.bfill()
                logger.info(f"✓ Preenchidas {missing_count} valores faltantes (backward fill)")
            else:
                raise ValueError(f"Estratégia desconhecida: {strategy}")
            
            return df
        except Exception as e:
            logger.error(f"Erro ao lidar com valores faltantes: {str(e)}")
            raise
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Renomear colunas
        
        Args:
            df: DataFrame
            mapping: Dicionário de mapeamento {coluna_antiga: coluna_nova}
            
        Returns:
            DataFrame com colunas renomeadas
        """
        try:
            df = df.rename(columns=mapping)
            logger.info(f"✓ Renomeadas {len(mapping)} colunas")
            return df
        except Exception as e:
            logger.error(f"Erro ao renomear colunas: {str(e)}")
            raise
    
    @staticmethod
    def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Selecionar apenas colunas específicas
        
        Args:
            df: DataFrame
            columns: Lista de colunas a manter
            
        Returns:
            DataFrame com apenas as colunas selecionadas
        """
        try:
            missing_cols = set(columns) - set(df.columns)
            if missing_cols:
                logger.warning(f"Colunas não encontradas: {missing_cols}")
            
            df = df[[col for col in columns if col in df.columns]]
            logger.info(f"✓ Selecionadas {len(df.columns)} colunas")
            return df
        except Exception as e:
            logger.error(f"Erro ao selecionar colunas: {str(e)}")
            raise
    
    @staticmethod
    def filter_rows(df: pd.DataFrame, condition: Callable[[pd.DataFrame], pd.Series]) -> pd.DataFrame:
        """
        Filtrar linhas baseado em condição
        
        Args:
            df: DataFrame
            condition: Função que retorna Series booleana
            
        Returns:
            DataFrame filtrado
        """
        try:
            initial_count = len(df)
            df = df[condition(df)]
            removed = initial_count - len(df)
            logger.info(f"✓ Filtradas {removed} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro ao filtrar linhas: {str(e)}")
            raise
    
    @staticmethod
    def convert_data_types(df: pd.DataFrame, dtype_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Converter tipos de dados
        
        Args:
            df: DataFrame
            dtype_mapping: Dicionário de mapeamento {coluna: tipo}
            
        Returns:
            DataFrame com tipos convertidos
        """
        try:
            for column, dtype in dtype_mapping.items():
                if column in df.columns:
                    try:
                        df[column] = df[column].astype(dtype)
                        logger.info(f"✓ Coluna {column} convertida para {dtype}")
                    except Exception as e:
                        logger.error(f"Erro ao converter {column} para {dtype}: {str(e)}")
            
            return df
        except Exception as e:
            logger.error(f"Erro ao converter tipos de dados: {str(e)}")
            raise
    
    @staticmethod
    def normalize_column(df: pd.DataFrame, column: str, method: str = "minmax") -> pd.DataFrame:
        """
        Normalizar coluna numérica
        
        Args:
            df: DataFrame
            column: Nome da coluna
            method: 'minmax' ou 'zscore'
            
        Returns:
            DataFrame com coluna normalizada
        """
        try:
            if column not in df.columns:
                logger.warning(f"Coluna {column} não encontrada")
                return df
            
            if method == "minmax":
                min_val = df[column].min()
                max_val = df[column].max()
                
                # Evitar divisão por zero
                if max_val == min_val:
                    logger.warning(f"Coluna {column} tem todos os valores iguais. Normalizando para 0.")
                    df[column] = 0
                else:
                    df[column] = (df[column] - min_val) / (max_val - min_val)
                
                logger.info(f"✓ Coluna {column} normalizada (minmax)")
            elif method == "zscore":
                mean = df[column].mean()
                std = df[column].std()
                
                # Evitar divisão por zero
                if std == 0:
                    logger.warning(f"Coluna {column} tem desvio padrão zero. Normalizando para 0.")
                    df[column] = 0
                else:
                    df[column] = (df[column] - mean) / std
                
                logger.info(f"✓ Coluna {column} normalizada (zscore)")
            else:
                raise ValueError(f"Método de normalização desconhecido: {method}")
            
            return df
        except Exception as e:
            logger.error(f"Erro ao normalizar coluna: {str(e)}")
            raise
    
    @staticmethod
    def add_calculated_column(df: pd.DataFrame, column_name: str, func: Callable) -> pd.DataFrame:
        """
        Adicionar coluna calculada
        
        Args:
            df: DataFrame
            column_name: Nome da nova coluna
            func: Função que calcula o valor
            
        Returns:
            DataFrame com nova coluna
        """
        try:
            df[column_name] = df.apply(func, axis=1)
            logger.info(f"✓ Adicionada coluna calculada: {column_name}")
            return df
        except Exception as e:
            logger.error(f"Erro ao adicionar coluna calculada: {str(e)}")
            raise
    
    @staticmethod
    def aggregate_data(df: pd.DataFrame, group_by: List[str], agg_func: Dict[str, str]) -> pd.DataFrame:
        """
        Agregar dados
        
        Args:
            df: DataFrame
            group_by: Colunas para agrupar
            agg_func: Dicionário de funções de agregação
            
        Returns:
            DataFrame agregado
        """
        try:
            df = df.groupby(group_by).agg(agg_func).reset_index()
            logger.info(f"✓ Dados agregados por {group_by}")
            return df
        except Exception as e:
            logger.error(f"Erro ao agregar dados: {str(e)}")
            raise
