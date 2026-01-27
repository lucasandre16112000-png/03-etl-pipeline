# etl/pipeline.py

import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import json

from .config.logger import setup_logger
from .config.settings import settings
from .extractors.data_extractor import DataExtractor
from .transformers.data_transformer import DataTransformer
from .loaders.data_loader import DataLoader
from .validators.data_validator import DataValidator

logger = setup_logger(__name__)

@dataclass
class PipelineStats:
    """Estatísticas do pipeline"""
    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    duplicates_removed: int = 0
    missing_values_handled: int = 0
    transformations_applied: int = 0
    execution_time: float = 0.0
    start_time: str = ""
    end_time: str = ""
    status: str = "pending"

class ETLPipeline:
    """Pipeline ETL profissional e robusto - 100% compatível com Windows"""
    
    def __init__(self):
        """Inicializar pipeline"""
        self.df = None
        self.stats = PipelineStats()
        self.validator = DataValidator()
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.validation_errors = []
        
        logger.info("✓ Pipeline ETL inicializado")
    
    def extract(self, file_path: str, file_type: Optional[str] = None, **kwargs) -> "ETLPipeline":
        """
        Extrair dados
        
        Args:
            file_path: Caminho do arquivo
            file_type: Tipo de arquivo
            **kwargs: Argumentos adicionais
            
        Returns:
            Self para encadeamento
        """
        try:
            self.df = self.extractor.extract(file_path, file_type, **kwargs)
            self.stats.total_records = len(self.df)
            logger.info(f"✓ Extração concluída: {self.stats.total_records} registros")
            return self
        except Exception as e:
            logger.error(f"✗ Erro na extração: {str(e)}")
            raise
    
    def remove_duplicates(self, subset: Optional[List[str]] = None, keep: str = "first") -> "ETLPipeline":
        """
        Remover registros duplicados
        
        Args:
            subset: Colunas para considerar
            keep: Qual duplicata manter
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            initial_count = len(self.df)
            self.df = self.transformer.remove_duplicates(self.df, subset, keep)
            self.stats.duplicates_removed = initial_count - len(self.df)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao remover duplicatas: {str(e)}")
            raise
    
    def handle_missing_values(self, strategy: str = "drop", fill_value: Any = None) -> "ETLPipeline":
        """
        Lidar com valores faltantes
        
        Args:
            strategy: Estratégia para lidar com valores faltantes
            fill_value: Valor para preencher
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            initial_count = len(self.df)
            self.df = self.transformer.handle_missing_values(self.df, strategy, fill_value)
            self.stats.missing_values_handled = initial_count - len(self.df)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao lidar com valores faltantes: {str(e)}")
            raise
    
    def rename_columns(self, mapping: Dict[str, str]) -> "ETLPipeline":
        """
        Renomear colunas
        
        Args:
            mapping: Dicionário de mapeamento
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.rename_columns(self.df, mapping)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao renomear colunas: {str(e)}")
            raise
    
    def select_columns(self, columns: List[str]) -> "ETLPipeline":
        """
        Selecionar colunas
        
        Args:
            columns: Lista de colunas
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.select_columns(self.df, columns)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao selecionar colunas: {str(e)}")
            raise
    
    def filter_rows(self, condition: Callable) -> "ETLPipeline":
        """
        Filtrar linhas
        
        Args:
            condition: Função de condição
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.filter_rows(self.df, condition)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao filtrar linhas: {str(e)}")
            raise
    
    def convert_types(self, dtype_mapping: Dict[str, str]) -> "ETLPipeline":
        """
        Converter tipos de dados
        
        Args:
            dtype_mapping: Dicionário de tipos
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.convert_data_types(self.df, dtype_mapping)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao converter tipos: {str(e)}")
            raise
    
    def normalize_column(self, column: str, method: str = "minmax") -> "ETLPipeline":
        """
        Normalizar coluna
        
        Args:
            column: Nome da coluna
            method: Método de normalização
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.normalize_column(self.df, column, method)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao normalizar coluna: {str(e)}")
            raise
    
    def add_column(self, column_name: str, func: Callable) -> "ETLPipeline":
        """
        Adicionar coluna calculada
        
        Args:
            column_name: Nome da coluna
            func: Função de cálculo
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.add_calculated_column(self.df, column_name, func)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao adicionar coluna: {str(e)}")
            raise
    
    def aggregate(self, group_by: List[str], agg_func: Dict[str, str]) -> "ETLPipeline":
        """
        Agregar dados
        
        Args:
            group_by: Colunas para agrupar
            agg_func: Funções de agregação
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.df = self.transformer.aggregate_data(self.df, group_by, agg_func)
            self.stats.transformations_applied += 1
            return self
        except Exception as e:
            logger.error(f"✗ Erro ao agregar dados: {str(e)}")
            raise
    
    def load(self, file_path: str, file_type: Optional[str] = None, **kwargs) -> "ETLPipeline":
        """
        Carregar dados
        
        Args:
            file_path: Caminho do arquivo
            file_type: Tipo de arquivo
            **kwargs: Argumentos adicionais
            
        Returns:
            Self para encadeamento
        """
        if self.df is None:
            raise ValueError("Nenhum dado para processar. Execute extract() primeiro.")
        
        try:
            self.loader.load(self.df, file_path, file_type, **kwargs)
            logger.info(f"✓ Carregamento concluído: {file_path}")
            return self
        except Exception as e:
            logger.error(f"✗ Erro no carregamento: {str(e)}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obter estatísticas do pipeline
        
        Returns:
            Dicionário com estatísticas
        """
        return asdict(self.stats)
    
    def save_stats(self, file_path: str) -> None:
        """
        Salvar estatísticas em arquivo JSON
        
        Args:
            file_path: Caminho do arquivo
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.get_stats(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ Estatísticas salvas em: {file_path}")
        except Exception as e:
            logger.error(f"✗ Erro ao salvar estatísticas: {str(e)}")
            raise
    
    def run(self, start_time: Optional[str] = None) -> None:
        """
        Marcar início da execução
        
        Args:
            start_time: Tempo de início (opcional)
        """
        if start_time is None:
            start_time = datetime.now().isoformat()
        
        self.stats.start_time = start_time
        self.stats.status = "running"
        logger.info(f"Pipeline iniciado em: {start_time}")
    
    def finish(self, execution_time: Optional[float] = None) -> None:
        """
        Marcar fim da execução
        
        Args:
            execution_time: Tempo de execução (opcional)
        """
        end_time = datetime.now().isoformat()
        self.stats.end_time = end_time
        self.stats.status = "completed"
        
        if execution_time is not None:
            self.stats.execution_time = execution_time
        
        logger.info(f"Pipeline concluído em: {end_time}")
        logger.info(f"Tempo total: {self.stats.execution_time:.2f}s")
