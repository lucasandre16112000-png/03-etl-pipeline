# tests/test_pipeline.py

import pytest
import pandas as pd
import json
import tempfile
from pathlib import Path
from etl.pipeline import ETLPipeline, PipelineStats

@pytest.fixture
def sample_csv_file():
    """Criar arquivo CSV de exemplo"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,name,email,age,salary\n")
        f.write("1,Alice,alice@example.com,25,50000\n")
        f.write("2,Bob,bob@example.com,30,60000\n")
        f.write("3,Charlie,charlie@example.com,35,70000\n")
        f.write("4,David,david@example.com,40,80000\n")
        f.write("5,Eve,eve@example.com,45,90000\n")
        return f.name

@pytest.fixture
def pipeline():
    """Criar instância do pipeline"""
    return ETLPipeline()

class TestETLPipeline:
    """Testes para o pipeline ETL"""
    
    def test_pipeline_initialization(self, pipeline):
        """Testar inicialização do pipeline"""
        assert pipeline.df is None
        assert pipeline.stats.total_records == 0
        assert pipeline.stats.transformations_applied == 0
    
    def test_extract(self, pipeline, sample_csv_file):
        """Testar extração de dados"""
        pipeline.extract(sample_csv_file)
        
        assert pipeline.df is not None
        assert len(pipeline.df) == 5
        assert pipeline.stats.total_records == 5
    
    def test_extract_chaining(self, pipeline, sample_csv_file):
        """Testar encadeamento de métodos"""
        result = pipeline.extract(sample_csv_file)
        
        assert result is pipeline
    
    def test_remove_duplicates(self, pipeline, sample_csv_file):
        """Testar remoção de duplicatas"""
        pipeline.extract(sample_csv_file)
        initial_count = len(pipeline.df)
        
        # Adicionar duplicata
        pipeline.df = pd.concat([pipeline.df, pipeline.df.iloc[[0]]], ignore_index=True)
        
        pipeline.remove_duplicates()
        
        assert len(pipeline.df) == initial_count
        assert pipeline.stats.duplicates_removed == 1
    
    def test_handle_missing_values(self, pipeline, sample_csv_file):
        """Testar tratamento de valores faltantes"""
        pipeline.extract(sample_csv_file)
        
        # Adicionar valores faltantes
        pipeline.df.loc[0, 'email'] = None
        
        pipeline.handle_missing_values(strategy="drop")
        
        assert len(pipeline.df) == 4
        assert pipeline.stats.missing_values_handled == 1
    
    def test_rename_columns(self, pipeline, sample_csv_file):
        """Testar renomeação de colunas"""
        pipeline.extract(sample_csv_file)
        
        mapping = {'id': 'employee_id', 'name': 'employee_name'}
        pipeline.rename_columns(mapping)
        
        assert 'employee_id' in pipeline.df.columns
        assert 'employee_name' in pipeline.df.columns
    
    def test_select_columns(self, pipeline, sample_csv_file):
        """Testar seleção de colunas"""
        pipeline.extract(sample_csv_file)
        
        columns = ['id', 'name', 'salary']
        pipeline.select_columns(columns)
        
        assert list(pipeline.df.columns) == columns
    
    def test_filter_rows(self, pipeline, sample_csv_file):
        """Testar filtragem de linhas"""
        pipeline.extract(sample_csv_file)
        
        pipeline.filter_rows(lambda df: df['age'] > 30)
        
        assert len(pipeline.df) == 3
        assert all(pipeline.df['age'] > 30)
    
    def test_convert_types(self, pipeline, sample_csv_file):
        """Testar conversão de tipos"""
        pipeline.extract(sample_csv_file)
        
        dtype_mapping = {'age': 'float', 'salary': 'int'}
        pipeline.convert_types(dtype_mapping)
        
        assert pipeline.df['age'].dtype == float
        assert pipeline.df['salary'].dtype == int
    
    def test_normalize_column(self, pipeline, sample_csv_file):
        """Testar normalização de coluna"""
        pipeline.extract(sample_csv_file)
        
        pipeline.normalize_column('age', method='minmax')
        
        assert pipeline.df['age'].min() >= 0
        assert pipeline.df['age'].max() <= 1
    
    def test_add_column(self, pipeline, sample_csv_file):
        """Testar adição de coluna"""
        pipeline.extract(sample_csv_file)
        
        pipeline.add_column('age_group', lambda row: 'Senior' if row['age'] >= 40 else 'Junior')
        
        assert 'age_group' in pipeline.df.columns
    
    def test_aggregate(self, pipeline, sample_csv_file):
        """Testar agregação de dados"""
        pipeline.extract(sample_csv_file)
        
        # Adicionar coluna de departamento
        pipeline.df['department'] = ['Sales', 'IT', 'Sales', 'HR', 'IT']
        
        pipeline.aggregate(['department'], {'salary': 'mean'})
        
        assert len(pipeline.df) == 3
    
    def test_load_csv(self, pipeline, sample_csv_file):
        """Testar carregamento em CSV"""
        pipeline.extract(sample_csv_file)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            output_file = f.name
        
        pipeline.load(output_file)
        
        # Verificar se arquivo foi criado
        assert Path(output_file).exists()
        
        # Limpar
        Path(output_file).unlink()
    
    def test_load_json(self, pipeline, sample_csv_file):
        """Testar carregamento em JSON"""
        pipeline.extract(sample_csv_file)
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_file = f.name
        
        pipeline.load(output_file)
        
        # Verificar se arquivo foi criado
        assert Path(output_file).exists()
        
        # Limpar
        Path(output_file).unlink()
    
    def test_get_stats(self, pipeline, sample_csv_file):
        """Testar obtenção de estatísticas"""
        pipeline.extract(sample_csv_file)
        pipeline.remove_duplicates()
        
        stats = pipeline.get_stats()
        
        assert stats['total_records'] == 5
        assert stats['transformations_applied'] == 1
    
    def test_save_stats(self, pipeline, sample_csv_file):
        """Testar salvamento de estatísticas"""
        pipeline.extract(sample_csv_file)
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            stats_file = f.name
        
        pipeline.save_stats(stats_file)
        
        # Verificar se arquivo foi criado
        assert Path(stats_file).exists()
        
        # Limpar
        Path(stats_file).unlink()
    
    def test_pipeline_chaining(self, pipeline, sample_csv_file):
        """Testar encadeamento completo do pipeline"""
        pipeline.extract(sample_csv_file) \
            .rename_columns({'id': 'employee_id'}) \
            .filter_rows(lambda df: df['age'] > 25) \
            .select_columns(['employee_id', 'name', 'salary'])
        
        assert 'employee_id' in pipeline.df.columns
        assert len(pipeline.df) == 4
        assert pipeline.stats.transformations_applied == 3
    
    def test_extract_without_data(self, pipeline):
        """Testar erro ao processar sem dados"""
        with pytest.raises(ValueError):
            pipeline.remove_duplicates()
