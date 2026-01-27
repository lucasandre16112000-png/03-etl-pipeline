# tests/test_transformers.py

import pytest
import pandas as pd
import numpy as np
from etl.transformers.data_transformer import DataTransformer

@pytest.fixture
def sample_dataframe():
    """Criar DataFrame de exemplo"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000],
        'department': ['Sales', 'IT', 'Sales', 'HR', 'IT']
    })

@pytest.fixture
def dataframe_with_duplicates():
    """Criar DataFrame com duplicatas"""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 3],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Charlie'],
        'email': ['alice@example.com', 'bob@example.com', 'bob@example.com', 'charlie@example.com', 'charlie@example.com']
    })

@pytest.fixture
def dataframe_with_missing():
    """Criar DataFrame com valores faltantes"""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', None, 'David', 'Eve'],
        'age': [25, None, 35, 40, 45],
        'salary': [50000, 60000, 70000, None, 90000]
    })

class TestDataTransformer:
    """Testes para o transformador de dados"""
    
    def test_remove_duplicates(self, dataframe_with_duplicates):
        """Testar remoção de duplicatas"""
        df = DataTransformer.remove_duplicates(dataframe_with_duplicates)
        
        assert len(df) == 3
        assert df['id'].nunique() == 3
    
    def test_remove_duplicates_subset(self, dataframe_with_duplicates):
        """Testar remoção de duplicatas com subset"""
        df = DataTransformer.remove_duplicates(dataframe_with_duplicates, subset=['id'])
        
        assert len(df) == 3
    
    def test_handle_missing_values_drop(self, dataframe_with_missing):
        """Testar remoção de valores faltantes"""
        df = DataTransformer.handle_missing_values(dataframe_with_missing, strategy="drop")
        
        assert len(df) == 2
        assert df.isnull().sum().sum() == 0
    
    def test_handle_missing_values_fill(self, dataframe_with_missing):
        """Testar preenchimento de valores faltantes"""
        df = DataTransformer.handle_missing_values(dataframe_with_missing, strategy="fill", fill_value=0)
        
        assert df.isnull().sum().sum() == 0
        assert df.loc[df['id'] == 3, 'name'].values[0] == 0
    
    def test_rename_columns(self, sample_dataframe):
        """Testar renomeação de colunas"""
        mapping = {'id': 'employee_id', 'name': 'employee_name'}
        df = DataTransformer.rename_columns(sample_dataframe, mapping)
        
        assert 'employee_id' in df.columns
        assert 'employee_name' in df.columns
        assert 'id' not in df.columns
    
    def test_select_columns(self, sample_dataframe):
        """Testar seleção de colunas"""
        columns = ['id', 'name', 'salary']
        df = DataTransformer.select_columns(sample_dataframe, columns)
        
        assert list(df.columns) == columns
    
    def test_filter_rows(self, sample_dataframe):
        """Testar filtragem de linhas"""
        df = DataTransformer.filter_rows(sample_dataframe, lambda df: df['age'] > 30)
        
        assert len(df) == 3
        assert all(df['age'] > 30)
    
    def test_convert_data_types(self, sample_dataframe):
        """Testar conversão de tipos de dados"""
        dtype_mapping = {'age': 'float', 'salary': 'int'}
        df = DataTransformer.convert_data_types(sample_dataframe, dtype_mapping)
        
        assert df['age'].dtype == float
        assert df['salary'].dtype == int
    
    def test_normalize_column_minmax(self, sample_dataframe):
        """Testar normalização minmax"""
        df = DataTransformer.normalize_column(sample_dataframe, 'age', method='minmax')
        
        assert df['age'].min() >= 0
        assert df['age'].max() <= 1
    
    def test_normalize_column_zscore(self, sample_dataframe):
        """Testar normalização zscore"""
        df = DataTransformer.normalize_column(sample_dataframe, 'age', method='zscore')
        
        assert abs(df['age'].mean()) < 0.01  # Próximo de 0
    
    def test_add_calculated_column(self, sample_dataframe):
        """Testar adição de coluna calculada"""
        df = DataTransformer.add_calculated_column(
            sample_dataframe,
            'age_group',
            lambda row: 'Senior' if row['age'] >= 40 else 'Junior'
        )
        
        assert 'age_group' in df.columns
        assert df.loc[df['age'] >= 40, 'age_group'].unique()[0] == 'Senior'
    
    def test_aggregate_data(self, sample_dataframe):
        """Testar agregação de dados"""
        df = DataTransformer.aggregate_data(
            sample_dataframe,
            group_by=['department'],
            agg_func={'salary': 'mean', 'age': 'count'}
        )
        
        assert len(df) == 3
        assert 'department' in df.columns
